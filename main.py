import discord
import json
import time
import random
from datetime import datetime, timedelta
import sys
import asyncio
import os
import keep_alive as k

os.system("pip install git+https://github.com/Rapptz/discord.py")

# --- load files ---
import for4
import emb

#pip install git+https://github.com/Rapptz/discord.py

sys.path.append("/home/runner/")
sys.path.append("/home/runner/pictures")
sys.path.append("/home/runner/spoon")

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready(self):
	print("-------")
	print(client.user.name, 'おきたでー')


@client.event
async def on_ready(self):
	print("-------")
	print(f"{client.user.name}おきたらしいわ")


# VC入退室ログ
# LINK https://note.nkmk.me/python-datetime-now-today/
@client.event
async def on_voice_state_update(member, before, after):
	if member.guild.id == for4.IDs[0] and before.channel != after.channel:
		now = datetime.now() + timedelta(hours=9)
		alert_ch = client.get_channel(for4.IDs[2])

		if before.channel is None:
			vcmsg = f'{now:%H:%M:%S} {member.name} {after.channel.name} イン'

		elif after.channel is None:
			vcmsg = f'{now:%H:%M:%S} {member.name} {before.channel.name} アウト'

		await alert_ch.send(vcmsg)


@client.event
async def on_message_delete(mes):
	def dlt(mes):
		msg = mes.content.id
		return mes.channel.delete(msg)

	if mes.author.id == for4.IDs[3]:
		msgid = mes.content.id
		await mes.channel.delete(msgid)


@client.event
async def on_message(mes):
	def EndsWith(m):
		return mes.content.endswith(m)

	def msg(m):
		return mes.channel.send(m)

	if mes.author.bot:
		return

	elif "spoon" in mes.content:
		await msg(file=discord.File(fushinsha))

	elif "だじゃれ" in mes.content:
		rnd = random.randint(0, len(for4.Jokes))
		await msg(for4.Jokes[rnd])

	elif EndsWith("笑") or EndsWith("w") or EndsWith("草"):
		rnd = random.randint(0, len(for4.Lol))
		await msg(for4.Lol[rnd])

	elif "ほんまに" in mes.content:
		rnd = random.randint(0, len(for4.Ofuro))
		await msg(random.choice(for4.Ofuro[rnd]))

	elif "不審者" in mes.content:
		fushinsha = "pictures/fushinsha.jpg"
		await msg("変なヤツかくほ", file=discord.File(fushinsha))

	elif "どうが" in mes.content:
		rnd = random.randint(0, len(for4.Vids))
		await msg(random.choice(for4.Vids[rnd]))

	elif mes.content == "おみくじ":
		rnd = random.randint(0, 100)

		# 大吉
		if rnd <= 100 and rnd >= 95:
			await msg(for4.Omikuji[0])

		# 中吉
		elif rnd < 95 and rnd >= 75:
			await msg(for4.Omikuji[1])

		# 吉
		elif rnd < 75 and rnd >= 40:
			await msg(for4.Omikuji[2])

		# 小吉
		elif rnd < 40 and rnd >= 20:
			await msg(for4.Omikuji[3])

		# 凶
		elif rnd < 20 and rnd >= 10:
			await msg(for4.Omikuji[3])

		# 大凶
		elif rnd < 10 and rnd >= 1:
			await msg(for4.Omikuji[5])

		# 帝凶
		else:
			await msg(for4.Omikuji[6])


k.keep_alive()
token = os.environ("KEY")
client.run(token)
