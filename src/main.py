import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

from for4 import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)
slash = SlashCommand(bot, sync_commands=True)


# ? 基 https://qiita.com/nyanmi-1828/items/54f165e77d4f7af770f7
class create_button(discord.ui.View):
    def __init__(self, _text: str):
        super().__init__()
        self.text: str = _text
        self.add_item(discord.ui.Button(label=self.text))


@bot.command()
async def ping(ctx):
    await ctx.reply('pong!')


@slash.slash(name='really honmany?', description='call me honmany')
async def honmany_really(ctx: SlashContext):
    await ctx.reply(f'hi, {ctx.author.display_name}')


@bot.event
async def on_raw_message_delete(ch: discord.channel, ctx):
    await ctx.ch.send('msg delete now')


if __name__ == '__main__':
    import os
    import dotenv

    dotenv.load_dotenv()
    try:
        token = os.environ['TOKEN']
    except KeyError:
        import pyenv
        token = pyenv.TOKEN

    @bot.event
    async def on_ready():
        print(f'{bot.user} is ready')

    bot.run(token)

#! https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html
