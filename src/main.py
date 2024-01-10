import discord
from discord.ext import commands
from discord import app_commands
from random import randint
import os
from datetime import datetime

from trrne.lottery import Lottery
from for4 import *
from emb import *
from trrne.trrne import *


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)

get_nick_filepath: str = lambda id: f'./nicks/{id}.txt'
get_point_filepath: str = lambda id: f'./points/{id}.txt'


ENCODING_UTF8 = 'utf-8'
REJECTED = 'rejected'


@tree.command(name='test', description='command for test')
async def cc(interaction: discord.Interaction):
    await interaction.response.send_message('testing', ephemeral=True)


@tree.command(name='user_info', description='ユーザー情報')
@app_commands.describe(member='メンバー')
async def user_info(interaction: discord.Interaction, member: discord.Member):
    user_id = member.id
    mc = member.created_at
    account_created = f'アカウント作成日時: {mc.year}/{mc.month}/{mc.day} {mc.hour}:{mc.minute}:{mc.second}'
    mj = member.joined_at
    server_joined = f'サーバー参加日時: {mj.year}/{mj.month}/{mj.day} {mj.hour}:{mj.minute}:{mj.second}'
    roles = ','.join(
        [role.mention for role in member.roles if role.name != '@everyone'])
    info_embed = discord.Embed(
        title=member.name,
        description=f'{user_id}\n{account_created}\n{server_joined}\n{roles}',
        colour=discord.Colour.green(),
        timestamp=datetime.now(),
    )
    info_embed.set_image(url=member.avatar.url)
    await interaction.response.send_message(embed=info_embed, ephemeral=True)


@tree.command(name='nicks_list', description='登録されているなまえのリスト')
@app_commands.describe(member='表示したいユーザー')
@app_commands.guild_only()
async def show_names(interaction: discord.Interaction, member: discord.Member):
    try:
        with open(get_nick_filepath(member.id), 'r', encoding=ENCODING_UTF8) as f:
            await interaction.response.send_message('\n'.join(f.read().split(' ')))
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='registered_users_list', description='登録されているユーザーリスト')
async def registered_users(interaction: discord.Interaction):
    try:
        users: list[str] = [
            f'<@{os.path.basename(file).removesuffix(".txt")}>' for file in os.listdir('./nicks')]
        counts: list[int] = []
        for user in users:
            with open(get_nick_filepath(delete_lump(user, ['<@', '>'])), 'r', encoding=ENCODING_UTF8) as f:
                counts.append(len(f.read().split(' ')))
        await interaction.response.send_message(embed=discord.Embed(
            title='登録されているユーザー',
            description='\n'.join(
                f'{user}: {count}' for user, count in zip(users, counts)),
            colour=discord.Colour.orange()
        ))
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='honmany', description='あいさつ')
@app_commands.guild_only()
async def honmany(interaction: discord.Interaction):
    try:
        with open(get_nick_filepath(interaction.user.id), 'r', encoding=ENCODING_UTF8) as f:
            names = f.read().split(' ')
            await interaction.response.send_message(f'{names[randint(0, len(names)-1)]}サン、コンニチハ！')
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='add_name', description='新しい名前を追加')
@app_commands.describe(target='対象のメンバー', addition='追加したい名前')
@app_commands.guild_only()
async def add_name(interaction: discord.Interaction, target: discord.Member, addition: str):
    try:
        with open(get_nick_filepath(target.id), 'a', encoding=ENCODING_UTF8) as f:
            f.write(f' {addition}')
            await interaction.response.send_message(f'success! added {addition} to nicknames list', ephemeral=True)
    except:
        await interaction.response.send_message(f'{REJECTED}: ユーザーIDが登録されていません', ephemeral=True)


# TODO 動作確認
@tree.command(name='remove_name', description='登録された名前を削除する')
@app_commands.describe(target='対象のメンバー', delete='削除したい名前')
@app_commands.guild_only()
async def delete_name(interaction: discord.Interaction, target: discord.Member, delete: str):
    try:
        with open(get_nick_filepath(target.id), 'w+', encoding=ENCODING_UTF8) as f:
            names = f.read().split(' ')
            names.remove(delete)
            f.write(str.join(' ', names))
            await interaction.response.send_message('success', ephemeral=True)
    except:
        await interaction.response.send_message(REJECTED, ephemeral=True)


@tree.command(name='lot_10', description='道徳46点の方向け10連くじ')
async def lot10(interaction: discord.Interaction):
    try:
        dst1: list[str] = []
        for i in range(10):
            index = Lottery.bst(kuji.weights())
            percentage = kuji.weights()[index]/kuji.total_weight()*100
            dst1.append(f'{i+1}: {kuji.subjects()[index]}({percentage}%)')
        await interaction.response.send_message('\n'.join(dst1))
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='lot_n', description='道徳n点の方向けn連くじ')
@app_commands.describe(count='回数')
async def lotn(interaction: discord.Interaction, count: int):
    counters: list[int] = [0] * kuji.length
    for _ in range(count):
        counters[Lottery.bst(kuji.weights)] += 1
    await interaction.response.send_message('\n'.join([
        f'{sub}: {count}' for sub, count in zip(kuji.subjects, counters) if count > 0
    ]))


@tree.command(name='lot_1', description='道徳100点の方向け単発くじ')
async def lot1(interaction: discord.Interaction):
    index = Lottery.bst(kuji.weights)
    dst = f'{kuji.subjects[index]}({kuji.weights[index]/kuji.total_weight*100}%)'
    await interaction.response.send_message(dst)


@tree.command(name='super_hyper_ultra_joke', description='おもろすぎるもの')
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(jokes[randint(0, len(jokes)-1)])


@tree.command(name='demonax', description='でもな、◯◯')
@app_commands.describe(name='member')
async def demona(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(dmn(name))


@tree.command(name='register_bet', description='登録する')
async def register_bet(interaction: discord.Interaction):
    try:
        if os.path.exists(get_point_filepath(interaction.user.id)):
            return await interaction.response.send_message('すでに登録されています。', ephemeral=True)

        with open(get_point_filepath(interaction.user.id), mode='w', encoding=ENCODING_UTF8) as f:
            f.write(str(init_point := 100))
            await interaction.response.send_message(f'アカウントを登録し、{init_point}ポイントを付与しました。', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(str(e), ephemeral=True)


@tree.command(name='delete_bet', description='削除する')
async def delete_bet(interaction: discord.Interaction):
    try:
        if not os.path.exists(get_point_filepath(interaction.user.id)):
            return await interaction.response.send_message('アカウントが登録されていません。', ephemeral=True)
        os.remove(get_point_filepath(interaction.user.id))
        await interaction.response.send_message('アカウントを削除しました。', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(str(e), ephemeral=True)


@tree.command(name='current_balance', description='所持しているポイントを表示')
async def current_balance(interaction: discord.Interaction):
    try:
        with open(get_point_filepath(interaction.user.id)) as f:
            await interaction.response.send_message(f'所持ポイント: {f.read()}', ephemeral=True)
    except:
        await interaction.response.send_message(f'アカウントが登録されていない可能性があります。"/{register_bet.name}"コマンドを実行してください。', ephemeral=True)


@tree.command(name='balance_ranking', description='ポイントランキング')
async def balance_ranking(interaction: discord.Interaction):
    pass


@tree.command(name='betting', description='所持しているポイントを表示')
async def do_bet(interaction: discord.Interaction):
    await interaction.response.send_message('comming not soon, maybe probably perhaps')


class Bet:
    def __init__(self, bot: discord.Client, tree: app_commands.CommandTree) -> None:
        self.bot = bot
        self.tree = tree
    


if __name__ == '__main__':
    @bot.event()
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

'''
https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html
http://www.not-enough.org/abe/manual/api-aa09/fileio.html
https://www.javadrive.jp/python/file/index9.html
'''
