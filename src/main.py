from datetime import datetime
import discord
from discord import app_commands
from random import randint
import os

from trrne.lottery import Lottery
from for4 import *
from emb import *
from trrne.trrne import *


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


get_nickname_filepath: str = lambda id: f'./nicknames/{id}.txt'


ENCODING_UTF8 = 'utf-8'
REJECTED = 'rejected'


@tree.command(name='test', description='command for test')
async def cc(interaction: discord.Interaction):
    await interaction.response.send_message('testing', ephemeral=True)


@tree.command(name='user_info', description='ユーザー情報')
@app_commands.describe(member='メンバー')
async def user_info(interaction: discord.Interaction, member: discord.Member):
    mc = member.created_at
    account_created = f'{mc.year}/{mc.month}/{mc.day} {mc.hour}:{mc.minute}:{mc.second}'
    mj = member.joined_at
    server_joined = f'{mj.year}/{mj.month}/{mj.day} {mj.hour}:{mj.minute}:{mj.second}'
    info_embed = discord.Embed(
        title=member.name,
        description=None,
        colour=discord.Colour.green(),
        timestamp=datetime.now(),
    )
    info_embed.description = f'\
        ユーザーid: {member.id}\n\
        アカウント作成日時: {account_created}\n\
        サーバー参加日: {server_joined}\n\
        ロール: {",".join([role.mention for role in member.roles if role.name != "@everyone"])}'
    info_embed.set_image(url=member.avatar.url)
    await interaction.response.send_message(embed=info_embed, ephemeral=True)


@tree.command(name='nickname_list', description='登録されているなまえのリスト')
@app_commands.describe(member='表示したいユーザー')
@app_commands.guild_only()
async def show_names(interaction: discord.Interaction, member: discord.Member):
    try:
        with open(get_nickname_filepath(member.id), 'r', encoding=ENCODING_UTF8) as f:
            await interaction.response.send_message('\n'.join(f.read().split(' ')))
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='registered_users_list', description='登録されているユーザーリスト')
async def registerd_users(interaction: discord.Interaction):
    try:
        users: list[str] = []
        for file in os.listdir('./nicknames'):
            users.append(f'<@{os.path.basename(file).removesuffix(".txt")}>')
        counts: list[int] = []
        for user in users:
            with open(get_nickname_filepath(delete_lump(user, ['<@', '>'])), 'r', encoding=ENCODING_UTF8) as f:
                counts.append(len(f.read().split(' ')))
        dst: list[str] = []
        for user, count in zip(users, counts):
            dst.append(f'{user}: {count}')
        await interaction.response.send_message(embed=discord.Embed(
            title='登録されているユーザー',
            description='\n'.join(dst),
            colour=discord.Colour.orange()
        ))
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='ほんめにー', description='あいさつ')
@app_commands.guild_only()
async def honmany(interaction: discord.Interaction):
    try:
        with open(get_nickname_filepath(interaction.user.id), 'r', encoding=ENCODING_UTF8) as f:
            names = f.read().split(' ')
        print(str.join(',', names))
        await interaction.response.send_message(f'{names[randint(0, len(names)-1)]}サン、コンニチハ！')
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='add_name', description='新しい名前を追加')
@app_commands.describe(target='対象のメンバー', addition='追加したい名前')
@app_commands.guild_only()
async def add_name(interaction: discord.Interaction, target: discord.Member, addition: str):
    # http://www.not-enough.org/abe/manual/api-aa09/fileio.html
    try:
        with open(get_nickname_filepath(target.id), 'a', encoding=ENCODING_UTF8) as f:
            f.write(f' {addition}')
            await interaction.response.send_message(f'success! added {addition} to nickname list', ephemeral=True)
    except:
        await interaction.response.send_message(f'{REJECTED}: ユーザーIDが登録されていません', ephemeral=True)


# TODO 動作確認
@tree.command(name='remove_name', description='登録された名前を削除する')
@app_commands.describe(target='対象のメンバー', delete='削除したい名前')
@app_commands.guild_only()
async def delete_name(interaction: discord.Interaction, target: discord.Member, delete: str):
    try:
        with open(get_nickname_filepath(target.id), 'w+', encoding=ENCODING_UTF8) as f:
            names = f.read().split(' ')
            names.remove(delete)
            f.write(str.join(' ', names))
            await interaction.response.send_message('success', ephemeral=True)
    except:
        await interaction.response.send_message('rejected', ephemeral=True)


@tree.command(name='くじ10口', description='道徳46点の方向け')
async def lot10(interaction: discord.Interaction):
    try:
        dst1: list[str] = []
        for i in range(10):
            index = Lottery.bst(kuji.weights())
            percentage = kuji.weights()[index]/kuji.total_weight()*100
            dst1.append(f'{i+1}: {kuji.subjects()[index]}({percentage}%)')
        await interaction.response.send_message('\n'.join(dst1))
    except:
        await interaction.response.send_message('rejected')


@tree.command(name='くじn口', description='道徳n点の方向け')
@app_commands.describe(count='回数')
async def lotn(interaction: discord.Interaction, count: int):
    counters: list[int] = [0] * kuji.length()
    for _ in range(count):
        index = Lottery.bst(kuji.weights())
        counters[index] += 1
    await interaction.response.send_message('\n'.join([
        f'{sub}: {count}' for (sub, count) in zip(kuji.subjects(), counters) if count > 0
    ]))


@tree.command(name='くじ1口', description='道徳100点の方向け')
async def lot1(interaction: discord.Interaction):
    index = Lottery.bst(kuji.weights())
    dst = f'{kuji.subjects()[index]}({kuji.weights()[index]/kuji.total_weight()*100}%)'
    await interaction.response.send_message(dst)


@tree.command(name='最先端ギャグ', description='おもろすぎるもの')
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(jokes[randint(0, len(jokes)-1)])


@tree.command(name='でもな', description='でもな、◯◯')
@app_commands.describe(name='member')
async def demona(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(demona(name))


if __name__ == '__main__':
    @bot.event
    async def on_ready():
        print('i\'m ready')
        await bot.change_presence(activity=discord.Game('なんか'))
        await tree.sync()

    try:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.environ['HONMANY_TOKEN']
    except:
        from pyenv import *
        token = HONMANY_TOKEN
    bot.run(token)

#! https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html
