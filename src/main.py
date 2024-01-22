import discord
from discord import app_commands
from random import randint
import os
import json
import pathlib

from trrne.lottery import *
from for4 import *
from emb import *
from trrne.trrne import *
from user_dict import *  # UserDict


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


class GetPath:
    @staticmethod
    def nicks(id: int) -> str:
        return f'./nicks/{id}.txt'

    @staticmethod
    def user(id: int) -> str:
        return f'../users/{id}.json'


REJECTED = 'rejected'


@tree.command(name='test', description='command for test')
async def cc(interaction: discord.Interaction):
    await interaction.response.send_message('testing', ephemeral=True)


@tree.command(name='user_info', description='ユーザー情報')
@app_commands.describe(member='メンバー')
async def user_info(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        title=member.name,
        description=f'ID: {member.id}\nRoles: {",".join([role.mention for role in member.roles if role.name != "@everyone"])}',
        colour=discord.Colour.orange()
    )
    embed.set_image(url=f'{member.avatar.url[:-4]}64')
    await interaction.response.send_message(str(member.avatar.url), embed=embed, ephemeral=True)


@tree.command(name='nicks_list', description='登録されているなまえのリスト')
@app_commands.describe(member='表示したいユーザー')
@app_commands.guild_only()
async def show_names(interaction: discord.Interaction, member: discord.Member):
    try:
        with open(GetPath.nicks(member.id), 'r') as f:
            await interaction.response.send_message('\n'.join(f.read().split(' ')))
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='registered_users', description='登録されているユーザーリスト')
async def registered_users(interaction: discord.Interaction):
    try:
        counts: list[int] = []
        for user in (users := [f'<@{os.path.basename(file).removesuffix(".txt")}>' for file in os.listdir('./nicks')]):
            with open(GetPath.nicks(delete_lump(user, ['<@', '>'])), 'r') as f:
                counts.append(len(f.read().split(' ')))
        await interaction.response.send_message(embed=discord.Embed(
            title='registered users list',
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
        with open(GetPath.nicks(interaction.user.id), 'r') as f:
            names = f.read().split(' ')
            await interaction.response.send_message(f'{names[randint(0, len(names)-1)]}サン、コンニチハ！')
    except:
        await interaction.response.send_message(REJECTED)


@tree.command(name='add_name', description='新しい名前を追加')
@app_commands.describe(target='対象のメンバー', addition='追加したい名前')
@app_commands.guild_only()
async def add_name(interaction: discord.Interaction, target: discord.Member, addition: str):
    try:
        with open(GetPath.nicks(target.id), 'a') as f:
            f.write(f' {addition}')
            await interaction.response.send_message(f'success! added {addition} to nicknames list', ephemeral=True)
    except:
        await interaction.response.send_message(f'{REJECTED}: ユーザーIDが登録されていません', ephemeral=True)


@tree.command(name='remove_name', description='登録された名前を削除する')
@app_commands.describe(target='対象のメンバー', delete='削除したい名前')
@app_commands.guild_only()
async def delete_name(interaction: discord.Interaction, target: discord.Member, delete: str):
    try:
        with open(GetPath.nicks(target.id), 'w+') as f:
            names = f.read().split(' ')
            names.remove(delete)
            f.write(str.join(' ', names))
            await interaction.response.send_message('success', ephemeral=True)
    except:
        await interaction.response.send_message(REJECTED, ephemeral=True)


@tree.command(name='lotn', description='道徳n点の方向けn連くじ')
@app_commands.describe(count='回数')
async def lotn(interaction: discord.Interaction, count: int):
    counters = [0] * kuji.length
    for _ in range(count):
        counters[Lottery.bst(kuji.weights)] += 1
    await interaction.response.send_message('\n'.join([
        f'{sub}: {count}' for sub, count in zip(kuji.subjects, counters) if count > 0
    ]))


@tree.command(name='lot1', description='道徳100点の方向け単発くじ')
async def lot1(interaction: discord.Interaction):
    index = Lottery.bst(kuji.weights)
    dst = f'{kuji.subjects[index]}({kuji.weights[index]/kuji.total_weight*100}%)'
    await interaction.response.send_message(dst)


@tree.command(name='lot10', description='道徳46点の方向け10連くじ')
async def lot10(interaction: discord.Interaction):
    stamps = LotteryPair([
        ('<:rainbowleo:1198626986269085767>', 0.2),  # rainbow
        ('<:carwakimoto:1198625297122214008>', 100)  # normal
    ])
    dst = ''
    for _ in range(10):
        dst += stamps.subjects[Lottery.bst(stamps.weights)]
    await interaction.response.send_message(dst)

    # dst1: list[str] = []
    # for i in range(10):
    #     index = Lottery.bst(kuji.weights())
    #     percentage = kuji.weights()[index]/kuji.total_weight()*100
    #     dst1.append(f'{i+1}: {kuji.subjects()[index]}({percentage}%)')
    # await interaction.response.send_message('\n'.join(dst1))


@tree.command(name='super_hyper_ultra_joke', description='おもろすぎるもの')
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(jokes[randint(0, len(jokes)-1)])


@tree.command(name='demonax', description='でもな、◯◯')
@app_commands.describe(name='member')
async def demonax(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(dmn(name))


@tree.command(name='iikax', description='いいか、◯◯')
@app_commands.describe(name='member')
async def iikax(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(iika(name))


@tree.command(name='register_user', description='ユーザーを登録する')
@app_commands.describe(member='member')
async def register_user(interaction: discord.Interaction, member: discord.Member):
    if os.path.exists(filepath := GetPath.user(member.id)):
        return await interaction.response.send_message('すでに登録されています', ephemeral=True)
    with open(filepath, 'x') as f:
        user_data = UserDict(
            name=member.name,
            id=member.id,
            created=member.created_at.now().__str__(),
            nicks=[],
            bet=GambleDict(
                enable=True,
                points=100
            )
        )
        user_data.get('nicks').append(member.display_name)
        json.dump(dict(user_data), f, indent=4)
        await interaction.response.send_message('登録しました', ephemeral=True)


@tree.command(name='delete_user', description='ユーザーを削除する')
@app_commands.describe(member='member')
async def delete_user(interaction: discord.Interaction, member: discord.Member):
    if not os.path.exists(filepath := GetPath.user(member.id)):
        return await interaction.response.send_message('登録されていません', ephemeral=True)
    os.remove(filepath)
    await interaction.response.send_message('削除しました。', ephemeral=True)


@tree.command(name='enable_bet', description='賭けを有効化する')
async def bet_enable(interaction: discord.Interaction):
    if not os.path.exists(filepath := GetPath.user(interaction.user.id)):
        return await interaction.response.send_message('ユーザーが登録されていません', ephemeral=True)
    # TODO なんか冗長な気がする 短くしたい
    with open(filepath, 'r') as f:
        pre_data = UserDict(json.load(f))
        pre_data['bet']['enable'] = True
        with open(filepath, 'w') as j:
            json.dump(pre_data, j, indent=4)
        await interaction.response.send_message('賭けを有効化しました。', ephemeral=True)


@tree.command(name='disable_bet', description='賭けを無効化する')
async def bet_disable(interaction: discord.Interaction):
    if not os.path.exists(filepath := GetPath.user(interaction.user.id)):
        return await interaction.response.send_message('ユーザーが登録されていません', ephemeral=True)
    with open(filepath, 'r') as f:
        pre_data = UserDict(json.load(f))
        pre_data['bet']['enable'] = False
        with open(filepath, 'w') as j:
            json.dump(pre_data, j, indent=4)
        await interaction.response.send_message('賭けを無効化しました。', ephemeral=True)


@tree.command(name='current_balance', description='所持しているポイントを表示')
async def current_balance(interaction: discord.Interaction):
    if not os.path.exists(path := GetPath.user(interaction.user.id)):
        return await interaction.response.send_message('ユーザーが登録されていません', ephemeral=True)
    with open(path, 'r') as f:
        await interaction.response.send_message(f'所持ポイント: {f.read()}', ephemeral=True)


@tree.command(name='balance_ranking', description='ポイントランキング')
async def balance_ranking(interaction: discord.Interaction):
    if len(os.listdir('./points')) < 1:
        await interaction.response.send_message('0登録', ephemeral=True)
    points: dict[str, int] = {}
    for d in os.listdir('./points'):
        with open(dir := d, mode='r') as f:
            points[f'<@{os.path.basename(dir).removesuffix(".txt")}>'] = f.read()
    try:
        sorted_points = sorted(points.items())
        await interaction.response.send_message(discord.Embed(
            title='Balance Ranking',
            description=[
                f'#{i+1} {sorted_points[i][0]}: {sorted_points[i][1]}' for i in range(len(sorted_points))],
            colour=discord.Colour.orange()
        ))
    except:
        raise Exception()


@tree.command(name='leokart', description='leokart')
async def leokart(interaction: discord.Interaction):
    stamps = LotteryPair([
        ('rainbowleo', 0.1),
        ('wakimotocar', 100)
    ])
    dst = ''
    for _ in range(10):
        dst += f':{stamps.subjects[Lottery.bst(stamps.weights)]}:'
    await interaction.response.send_message(dst)


@tree.command(name='betting', description='所持しているポイントを表示')
@app_commands.describe(amount='量')
async def do_bet(interaction: discord.Interaction, amount: int):
    with open(GetPath.user(interaction.user.id), 'r') as f:
        if amount > (remain_point := (player_data := UserDict(json.load(f)))['bet']['points']):
            return await interaction.response.send_message(f'残金が足りません。(残り{remain_point})')


class MyBot:
    def __init__(self, token_key: str) -> None:
        self.token_key = token_key

    def load_environ(self) -> str:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            return os.environ[self.token_key]
        except:
            import pyenv
            return pyenv.environ[self.token_key]


if __name__ == '__main__':
    @bot.event
    async def on_ready():
        print('i\'m ready')
        await bot.change_presence(activity=discord.Game('なんか'), status=discord.Status.idle)
        await tree.sync()

    mine = MyBot('HONMANY_TOKEN')
    bot.run(mine.load_environ())

'''
dpyドキュメント https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html

https://note.nkmk.me/python-file-io-open-with
http://www.not-enough.org/abe/manual/api-aa09/fileio.html
https://www.javadrive.jp/python/file/index9.html
'''
