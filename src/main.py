import discord
from discord import app_commands
from random import randint
import numpy as np

from trrne.lottery import Lottery
from trrne.m import M
from for4 import *
from emb import *


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


def nickname_file_path(id: int):
    return f'./nicknames/{id}.txt'


ENCODE = 'utf-8'


@tree.command(name='aa', description='bb')
async def cc(action: discord.Interaction):
    raise Exception('dd')


@tree.command(name='ほんめにー', description='あいさつ')
@app_commands.guild_only()
async def honmany(action: discord.Interaction):
    try:
        with open(nickname_file_path(action.user.id), 'r', encoding=ENCODE) as f:
            names = f.read().split(' ')
        print(str.join(',', names))
        await action.response.send_message(f'{names[randint(0, len(names)-1)]}サン、コンニチハ！')
    except FileNotFoundError as e:
        raise e


@tree.command(name='名前追加', description='新しい呼び名を追加')
@app_commands.describe(target='対象のメンバー', addition='追加したい名前')
async def add_name(action: discord.Interaction, target: discord.Member, addition: str):
    # http://www.not-enough.org/abe/manual/api-aa09/fileio.html
    try:
        with open(nickname_file_path(target.id), 'a', encoding=ENCODE) as f:
            f.write(f' {addition}')
            await action.response.send_message('success', ephemeral=True)
    except:
        await action.response.send_message('rejected', ephemeral=True)


# TODO 動作確認
@tree.command(name='名前削除', description='登録された名前を削除する')
@app_commands.describe(target='対象のメンバー', delete='削除したい名前')
async def delete_name(action: discord.Interaction, target: discord.Member, delete: str):
    try:
        with open(nickname_file_path(target.id), 'w+', encoding=ENCODE) as f:
            names = f.read().split(' ')
            names.remove(delete)
            f.write(str.join(' ', names))
            await action.response.send_message('success', ephemeral=True)
    except:
        await action.response.send_message('rejected', ephemeral=True)


@tree.command(name='くじ10口', description='道徳46点の方向け')
async def lot10(action: discord.Interaction):
    dst: str = ''
    for i in range(10):
        index = Lottery.bst(kuji.weights())
        dst += f'{i+1}: {kuji.subjects()[index]}({kuji.weights()[index]/kuji.total_weight()*100}%)' + \
            ('\n' if i < 10 else '')
    await action.response.send_message(dst)


@tree.command(name='くじn口', description='道徳46点の方向け')
@app_commands.describe(count='回数')
async def lotn(action: discord.Interaction, count: int):
    dst: str = ''
    count = np.abs(count)
    for i in range(count):
        index = Lottery.bst(kuji.weights())
        per = M.floor(kuji.weights()[index]/kuji.total_weight()*100, 2)
        dst += f'{i+1}: {kuji.subjects()[index]}({per}%)' + \
            ('\n' if i < count else '')
    await action.response.send_message(dst if dst.__len__() < 2000 else dst[:2000-1])


@tree.command(name='くじ1口', description='道徳100点の方向け')
async def lot(action: discord.Interaction):
    index = Lottery.bst(kuji.weights())
    dst = f'{kuji.subjects()[index]}({kuji.weights()[index]/kuji.total_weight()*100}%)'
    await action.response.send_message(dst)


@tree.command(name='最先端ギャグ', description='おもろすぎるもの')
async def joke(action: discord.Interaction):
    await action.response.send_message(jokes[randint(0, len(jokes)-1)])


@tree.command(name='でもな', description='でもな、◯◯')
@app_commands.describe(name='member')
async def demona(action: discord.Interaction, name: str):
    await action.response.send_message(demo(name))


if __name__ == '__main__':
    @bot.event
    async def on_ready():
        print('i\'m ready')
        await bot.change_presence(activity=discord.Game('active honmany!'))
        await tree.sync()

    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        token = os.environ['HONMANY_TOKEN']
    except:
        from pyenv import *
        token = HONMANY_TOKEN
    bot.run(token)

#! https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html
