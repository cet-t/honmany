import discord
from discord import app_commands
import numpy as np
import random

from trrne.lottery import Lottery
from for4 import *

bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


# @tree.command(name='hello', description='honmany!')
# async def hello(action: discord.Interaction):
#     await action.response.send_message('hello honmany!')


@tree.command(name='くじ', description='あわわ')
async def lot(action: discord.Interaction):
    #     index = Lottery.bst(kuji.weights())
    #     dst = f'{kuji.subjects()[index]}({int(np.floor(kuji.weights()[index]/kuji.total_weight()*100))}%)'
    #     await action.response.send_message(dst)

    dst: str = ''
    for i in range(10):
        index = Lottery.bst(kuji.weights())
        dst += str(i+1) + ': ' + kuji.subjects()[index] + '(' + str(int(
            np.floor(kuji.weights()[index]/kuji.total_weight()*100))) + '%)'
        if i < 10:
            dst += '\n'
    await action.response.send_message(dst)


@tree.command(name='最先端ギャグ', description='おもろすぎるもの')
async def joke(action: discord.Interaction):
    await action.response.send_message(jokes[random.randint(0, len(jokes))])

if __name__ == '__main__':
    import os
    # import dotenv

    # dst: str = ''
    # for i in range(10):
    #     dst += kuji.subjects[Lottery.bst(kuji.weights())]+'\n'
    # print(dst)

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game('active honmany!'))
        await tree.sync()

    # dotenv.load_dotenv()
    # token = os.environ['TOKEN']
    # もろ晒し
    token = 'NzM4NjczNzA5ODAzNTAzNjc4.GwoRrb.Pg8zhhaLw9l8XDn17vQHZc2hVNJEpAEeZ8HwOY' 
    bot.run(token)

#! https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html
