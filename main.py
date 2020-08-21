from discord.ext.commands import Bot
from discord.ext import commands
import discord
import http.client
import requests
import json
import random
import sys
import traceback
import asyncio
import datetime
from datetime import datetime
import jishaku

bot = commands.Bot(command_prefix="+", case_insensitive=True)
bot.owner_ids = {680519129219727380}

countmessages = False
alltimemsg = {}
updatemsg = []
msgidinstorage = {}
storage = None
trigger_chan = None
log = None
lb_channel = None
lb_msg = None
dawn = None

def get_key(val): 
    for key, value in alltimemsg.items(): 
         if val == value: 
             return key 

def fetch_top_members():
	msgcount = alltimemsg.copy()
	msgdata_values = list(alltimemsg.values())
	msgdata_values.sort(reverse=True)
	print(msgcount)
	d = 1
	top_members = " " 
	while d < 21:
		idd = None
		try:
			for key, value in msgcount.items(): 
				if msgdata_values[0] == value: 
					idd = int(key)
			user = bot.get_user(idd)
			top_members = top_members + "\n**{}.** {} | **{}** messages".format(d, user.mention, msgdata_values[0])
		except:
			top_members = top_members + "\n**{}.** \"N/A (LEFT THE SERVER)\" | **{}** messages".format(d, msgdata_values[0])
		del msgdata_values[0]
		del msgcount[idd]
		d += 1
	return top_members


@bot.event
async def on_ready():
	global countmessages
	global storage
	global trigger_chan
	global log
	storage = bot.get_channel(668462634634575905)
	trigger_chan = bot.get_channel(728009012028768257)
	log = bot.get_channel(729058195330433094)
	lb_channel = bot.get_channel(745266529695957042)
	lb_msg = await lb_channel.fetch_message(746295619974463499)
	dawn = bot.get_guild(699268126008672259)
	async for message in trigger_chan.history(limit=1):
		if message.content == "reset":
			print("Resuming resetting...")
			async for message in storage.history(limit=None):
				x = message.content.split("|")
				alltimemsg[int(x[0])] = int(x[1])
				msgidinstorage[int(x[0])] = message.id
			a = fetch_top_members()
			embed = discord.Embed(description="{}".format(a), color=0x000000)
			embed.set_footer(text="WEEKLY RESET | Seeing this means that the message leaderboard has been reset for its weekly reset.")
			await log.send(embed=embed)
			async for message in storage.history(limit=None):
				await message.delete()
			async for message in trigger_chan.history(limit=10):
				await message.delete()
			alltimemsg.clear()
			updatemsg.clear()
			msgidinstorage.clear()
			countmessages = True
			while True:
				for item in updatemsg:
					message = await storage.fetch_message(msgidinstorage[item])
					await message.edit(content=f"{item}|{alltimemsg[item]}")
				await asyncio.sleep(10)
			return
	async for message in storage.history(limit=None):
		x = message.content.split("|")
		alltimemsg[int(x[0])] = int(x[1])
		msgidinstorage[int(x[0])] = message.id
	countmessages = True
	print("Ready!")
	while True:
		for item in updatemsg:
			message = await storage.fetch_message(msgidinstorage[item])
			await message.edit(content=f"{item}|{alltimemsg[item]}")
		try:
			a = fetch_top_members()
		except:
			embed = discord.Embed(description="There's not enough ranked people this week to display the leaderboard. At least 10 people need to be ranked.", color=0x000000)
			embed.set_thumbnail(url=dawn.icon_url)
			await lb_msg.edit(content="**To check your rank/messages, you can do ``+rank`` (or ``+r`` for short). You can also check someone else's rank with the same command.**", embed=embed)
			await asyncio.sleep(60)
			continue
		embed = discord.Embed(description=a, color=0x000000)
		embed.set_author(name="dawn's weekly leaderboard", icon_url=bot.user.avatar_url)
		embed.set_thumbnail(url=dawn.icon_url)
		embed.set_footer(text="Resets every Sunday!")
		await lb_msg.edit(content="**To check your rank/messages, you can do ``+rank`` (or ``+r`` for short). You can also check someone else's rank with the same command.**", embed=embed)
		await asyncio.sleep(10)
				
@bot.event
async def on_message(m):
	global countmessages
	mid = m.author.id
	if m.channel.id == 728009012028768257 and m.content == "reset":
			countmessages = False
			print("Starting resetting...")
			a = fetch_top_members()
			embed = discord.Embed(description="{}".format(a), color=0x000000)
			embed.set_footer(text="WEEKLY RESET | Seeing this means that the message leaderboard has been reset for its weekly reset.")
			await log.send(embed=embed)
			async for message in storage.history(limit=None):
				await message.delete()
			async for message in trigger_chan.history(limit=10):
				await message.delete()
			alltimemsg.clear()
			updatemsg.clear()
			msgidinstorage.clear()
			countmessages = True
			return
	if countmessages and m.guild is not None and m.guild.id == 699268126008672259 and m.author.id != bot.user.id and m.author.bot == False and m.channel.id == 739293045044019301:
		try:
			msgs = alltimemsg[mid]
			alltimemsg[mid] = msgs + 1
		except:
			alltimemsg[mid] = 1
			a = await storage.send(f"{m.author.id}|1")
			msgidinstorage[mid] = a.id
		if mid not in updatemsg:
			updatemsg.append(mid)

	await bot.process_commands(m)

@bot.command(aliases=["r"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def rank(ctx, user: discord.Member):
	try:
		msgcount = alltimemsg[user.id]
	except:
		await ctx.send(f"{ctx.message.author.mention}, seems like that user isn't ranked yet.")
		return
	msgdata_values = list(alltimemsg.values())
	msgdata_values.sort(reverse=True)
	d = len(msgdata_values)
	e = 0
	pos = None
	while e <= d:
		if msgdata_values[e] == alltimemsg[user.id]:
			pos = e
			break
		e += 1
	pos += 1
	embed = discord.Embed(description="has sent **{}** messages this week.\n\nThey're ranked **{}** out of **{}** ranked people this week.".format(msgcount, pos, len(alltimemsg)))
	embed.set_author(name="{}".format(user.display_name), icon_url=user.avatar_url)
	await ctx.send(embed=embed)

@rank.error
async def rank_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		try:
			msgcount = alltimemsg[ctx.message.author.id]
		except:
			await ctx.send("Seems like you aren't ranked yet.")
			return
		msgdata_values = list(alltimemsg.values())
		msgdata_values.sort(reverse=True)
		d = len(msgdata_values)
		e = 0
		pos = None
		while e <= d:
			if msgdata_values[e] == alltimemsg[ctx.message.author.id]:
				pos = e
				break
			e += 1
		pos += 1
		embed = discord.Embed(description="has sent **{}** messages this week.\n\nThey're ranked **{}** out of **{}** ranked people this week.".format(msgcount, pos, len(alltimemsg)))
		embed.set_author(name="{}".format(ctx.message.author.display_name), icon_url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.BadArgument):
		await ctx.send(f"**{ctx.message.author.display_name_}**, user not found.")
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"**{ctx.message.author.display_name}**, slow down! you can use this command again in **{round(error.retry_after, 1)}**s.")
	else:
		print('Ignoring exception in command av:', file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		embed = discord.Embed(description="{}".format(error), color=0x000000)
		await ctx.send("uh, oops, i guess?", embed=embed)

#@bot.command(aliases=["lb"])
#@commands.cooldown(1, 10, commands.BucketType.guild)
#async def leaderboard(ctx):
#	a = fetch_top_members()
#	embed = discord.Embed(description=a, color=0x000000)
#	embed.set_author(name="babi's weekly leaderboard", icon_url=bot.user.avatar_url)
#	embed.set_footer(text="Resets every Sunday!")
#	await ctx.send(embed=embed)

#@leaderboard.error
#async def leaderboard_error(ctx, error):
#	if isinstance(error, commands.CommandOnCooldown):
#		await ctx.send(f"**{ctx.message.author.display_name}**, slow down! you can use this command again in **{round(error.retry_after, 1)}**s.\n\n**note: the cooldown for this command is for everyone in the server, meaning that once someone uses the command, everyone is on cooldown.**\nwhy? because we don't want to overload the bot, do we?")
#	else:
#		print('Ignoring exception in command av:', file=sys.stderr)
#		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
#		embed = discord.Embed(description="There's not enough ranked people this week to display the leaderboard. At least 10 people need to be ranked.".format(error), color=0x000000)
#		await ctx.send("{}".format(ctx.message.author.mention), embed=embed)

bot.load_extension("jishaku")  
bot.run("NzQ2MjkwNjEzMTc5MjUyODg4.Xz-LSw.JGaqhrzTaL8KFpmi_h-adgDJoCI")

