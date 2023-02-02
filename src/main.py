import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.reply("pong!")


# class CreateButton(discord.ui.View):
#     def __init__(self):
#         super().__init__()

#     @discord.ui.button(label="ボタンです")
#     async def return_message(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.send_message("折り返しのメッセージだよ")


# class button_(commands.Bot):
#     def __init__(self):
#         super().__init__()


# ? 基 https://qiita.com/nyanmi-1828/items/54f165e77d4f7af770f7
class creat_button(discord.ui.View):
    def __init__(self, _text: str):
        super().__init__()
        self.text: str = _text
        self.add_item(discord.ui.Button(label=self.text))


@bot.command()
@discord.ui.button()
async def botan(ctx, btn: discord.ui.button):
    await ctx.send(view=creat_button("botan"))
    await btn.interaction.response.send_message("bobotantan")

#! ボタンを実装する


@bot.command()
async def b(ctx: commands.Context):
    await ctx.send(view=creat_button("ぶっとん"))


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    try:
        token = os.environ["TOKEN"]
    except KeyError:
        token = "NzM4NjczNzA5ODAzNTAzNjc4.GyiREr.nDBWKYwGtRWY0qTtmcfPhHkoK-4Gk6D6sBX0G0"

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready")

    bot.run(token)

#! document
#! https://discordpy.readthedocs.io/ja/stable/ext/commands/index.html
