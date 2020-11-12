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

bot = commands.Bot(command_prefix="a!", case_insensitive=True)
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
ice = None

def get_key(val): 
    for key, value in alltimemsg.items(): 
         if val == value: 
             return key 

def fetch_top_members_lb():
	msgcount = alltimemsg.copy()
	msgdata_values = list(alltimemsg.values())
	msgdata_values.sort(reverse=True)
	print(msgcount)
	d = 1
	top_members = " " 
	while d < 11:
		idd = None
		try:
			for key, value in msgcount.items(): 
				if msgdata_values[0] == value: 
					idd = int(key)
			user = bot.get_user(idd)
			top_members = top_members + "\n**{}.** {} | **{}** messages".format(d, user.mention, msgdata_values[0])
		except:
			top_members = top_members + "\n**{}.** \"? (User left the server)\" | **{}** messages".format(d, msgdata_values[0])
		del msgdata_values[0]
		del msgcount[idd]
		d += 1
	return top_members

def fetch_top_members_msg():
	msgcount = alltimemsg.copy()
	msgdata_values = list(alltimemsg.values())
	msgdata_values.sort(reverse=True)
	print(msgcount)
	d = 1
	top_members = " " 
	while d < 26:
		idd = None
		try:
			for key, value in msgcount.items(): 
				if msgdata_values[0] == value: 
					idd = int(key)
			user = bot.get_user(idd)
			top_members = top_members + "\n**{}.** {} | **{}** messages".format(d, user.mention, msgdata_values[0])
		except:
			top_members = top_members + "\n**{}.** \"? (User left the server)\" | **{}** messages".format(d, msgdata_values[0])
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
	#storage = bot.get_channel(769971712904527934)
	trigger_chan = bot.get_channel(728009012028768257)
	log = bot.get_channel(739760112725524522)
	lb_channel = bot.get_channel(760418426455195668)
	#lb_channel = bot.get_channel(769971862251634688)
	lb_msg = await lb_channel.fetch_message(762548536553635840)
	#lb_msg = await lb_channel.fetch_message(769971918111375370)
	ice = bot.get_guild(734867158475079690)
	temp_numb_counter = 0
	async for message in trigger_chan.history(limit=None):
		if message.content == "reset":
			temp_numb_counter += 1
		if temp_numb_counter > 1:
			print("Resuming resetting...")
			async for message in storage.history(limit=None):
				x = message.content.split("|")
				alltimemsg[int(x[0])] = int(x[1])
				msgidinstorage[int(x[0])] = message.id
			msgcount = alltimemsg.copy()
			msgdata_values = list(alltimemsg.values())
			msgdata_values.sort(reverse=True)
			user = None
			msg_count = 0
			for key, value in msgcount.items(): 
				if msgdata_values[0] == value: 
					user = bot.get_user(idd)
					msg_count = value
			await log.send(f"**LEADERBOARD RESET** | Congratulations to {user.mention} for reaching and maintaining position 1 on the leaderboard, ending with **{msg_count} messages**. The leaderboard will now reset.")
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
			a = fetch_top_members_msg()
		except:
			embed = discord.Embed(description="There's not enough ranked people to display the leaderboard. At least 25 people need to be ranked.", color=0x000000)
			embed.set_thumbnail(url=ice.icon_url)
			await lb_msg.edit(content="**To check your rank/messages, you can do ``a!rank`` (or ``a!r`` for short). You can also check someone else's rank with the same command. You may also use ``a!lb`` to bring up a shorter leaderboard anywhere.**", embed=embed)
			await asyncio.sleep(60)
			continue
		embed = discord.Embed(description=a, color=0x000000)
		embed.set_author(name="ice's message leaderboard", icon_url=bot.user.avatar_url)
		embed.set_thumbnail(url=ice.icon_url)
		embed.set_footer(text="Resets every 2 weeks on Sunday!")
		await lb_msg.edit(content="**To check your rank/messages, you can do ``a!rank`` (or ``a!r`` for short). You can also check someone else's rank with the same command. You may also use ``a!lb`` to bring up a shorter leaderboard anywhere.**", embed=embed)
		await asyncio.sleep(15)
				
@bot.event
async def on_message(m):
	global countmessages
	mid = m.author.id
	if m.channel.id == 728009012028768257 and m.content == "reset":
			temp_numb_counter = 0
			async for message in trigger_chan.history(limit=None):
				if message.content == "reset":
					temp_numb_counter += 1
				if temp_numb_counter > 1:
					countmessages = False
					print("Starting resetting...")
					msgcount = alltimemsg.copy()
					msgdata_values = list(alltimemsg.values())
					msgdata_values.sort(reverse=True)
					user = None
					msg_count = 0
					for key, value in msgcount.items(): 
						if msgdata_values[0] == value: 
							user = bot.get_user(idd)
							msg_count = value
					await log.send(f"**LEADERBOARD RESET** | Congratulations to {user.mention} for reaching and maintaining position 1 on the leaderboard, ending with **{msg_count} messages**. The leaderboard will now reset.")
					async for message in storage.history(limit=None):
						await message.delete()
					async for message in trigger_chan.history(limit=10):
						await message.delete()
					alltimemsg.clear()
					updatemsg.clear()
					msgidinstorage.clear()
					countmessages = True
					return
	if countmessages and m.guild is not None and m.guild.id == 734867158475079690 and m.author.id != bot.user.id and m.author.bot == False and "chat" in m.channel.name:
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
	embed = discord.Embed(description="**{}** has sent **{}** messages.\n\nThey're ranked **{}** out of **{}** ranked people.".format(user.display_name, msgcount, pos, len(alltimemsg)))
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
		embed = discord.Embed(description="**{}** has sent **{}** messages.\n\nThey're ranked **{}** out of **{}** ranked people.".format(ctx.message.author.display_name, msgcount, pos, len(alltimemsg)))
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

@bot.command(aliases=["lb"])
@commands.cooldown(1, 10, commands.BucketType.guild)
async def leaderboard(ctx):
	a = fetch_top_members_lb()
	embed = discord.Embed(description=a, color=0x000000)
	embed.set_author(name="ice's message leaderboard", icon_url=bot.user.avatar_url)
	embed.set_footer(text="Resets every 2 weeks on Sunday!")
	await ctx.send(embed=embed)

@leaderboard.error
async def leaderboard_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"**{ctx.message.author.display_name}**, slow down! you can use this command again in **{round(error.retry_after, 1)}**s.\n\n**note: the cooldown for this command is for everyone in the server, meaning that once someone uses the command, everyone is on cooldown.**\nwhy? because we don't want to overload the bot, do we?")
	else:
		print('Ignoring exception in command av:', file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		embed = discord.Embed(description="There's not enough ranked people to display the leaderboard. At least 10 people need to be ranked.".format(error), color=0x000000)
		await ctx.send("{}".format(ctx.message.author.mention), embed=embed)
		
@bot.command(help="USAGE: a!status [o/i/d] [p/w/l] [message]\n\nChanges the bot's status. Online, idle or do not disturb. Playing, watching or listening to. ⚠️ THIS DOES NOT APPLY FOR THE STREAMING STATUS. The correct usage for the streaming status is: a!status [s/streaming] [twitch_link] [status].\n\nExample: a!status o w you sleep..")
@commands.has_permissions(administrator=True)
async def status(ctx, a, b, *, status: str = " "):
    if len(a) != 0:
        if (a == "s" or a == "streaming"):
            bb = str(b)
            await bot.change_presence(activity=discord.Streaming(name=status, url=bb))
            embed = discord.Embed(description="Status changed. \n**Streaming**\n**on [this channel]({}): `{}`**".format(b, status), color=0x000000)
        elif (a == "o" or a == "online") and (b == "p" or b == "playing"):
            embed = discord.Embed(description="Status changed. \n**Online**\n**Playing {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.playing))
        elif (a == "o" or a == "online") and (b == "w" or b == "watching"):
            embed = discord.Embed(description="Status changed. \n**Online**\n**Watching {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.watching))
        elif (a == "o" or a == "online") and (b == "l" or b == "listening"):
            embed = discord.Embed(description="Status changed. \n**Online**\n**Listening to {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.listening))
        elif (a == "i" or a == "idle") and (b == "p" or b == "playing"):
            embed = discord.Embed(description="Status changed. \n**Idle**\n**Playing {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.idle,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.playing))
        elif (a == "i" or a == "idle") and (b == "w" or b == "watching"):
            embed = discord.Embed(description="Status changed. \n**Idle**\n**Watching {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.idle,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.watching))
        elif (a == "i" or a == "idle") and (b == "l" or b == "listening"):
            embed = discord.Embed(description="Status changed. \n**Idle**\n**Listening to {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.idle,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.listening))
        elif (a == "d" or a == "dnd") and (b == "p" or b == "playing"):
            embed = discord.Embed(description="Status changed. \n**Do Not Disturb**\n**Playing {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(name='{}'.format(status),
                                                                                           type=discord.ActivityType.playing))
        elif (a == "d" or a == "dnd") and (b == "w" or b == "watching"):
            embed = discord.Embed(
                description="Status changed. \n**Do Not Disturb**\n**Watching {}**".format(status), color=0x000000)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(name='{}'.format(status),
                                                                                           type=discord.ActivityType.watching))
        elif (a == "d" or a == "dnd") and (b == "l" or b == "listening"):
            embed = discord.Embed(
                description="Status changed. \n**Do Not Disturb**\n**Listening to {}**".format(status),
                color=0x000000)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(name='{}'.format(status),
                                                                                           type=discord.ActivityType.listening))
        elif a == "o" or a == "online":
            if len(a) == 1:
                statuss = ctx.message.content[9:]
            elif len(a) == 6:
                statuss = ctx.message.content[14:]
            embed = discord.Embed(description="Status changed. \n**Online**\n**Playing {}**".format(statuss),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(statuss),
                                                                type=discord.ActivityType.playing))
            embed2 = discord.Embed(description="Since you didn't provide a valid **status_msg**, I chose the default one: **Playing**.", color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
        elif a == "i" or a == "idle":
            if len(a) == 1:
                statuss = ctx.message.content[9:]
            elif len(a) == 4:
                statuss = ctx.message.content[12:]
            embed = discord.Embed(description="Status changed. \n**Idle**\n**Playing {}**".format(statuss),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.idle,
                                      activity=discord.Activity(name='{}'.format(statuss),
                                                                type=discord.ActivityType.playing))
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_msg**, I chose the default one: **Playing**.",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
        elif a == "d" or a == "dnd":
            if len(a) == 1:
                statuss = ctx.message.content[9:]
            elif len(a) == 3:
                statuss = ctx.message.content[11:]
            embed = discord.Embed(
                description="Status changed. \n**Do Not Disturb**\n**Playing {}**".format(statuss), color=0x000000)
            await bot.change_presence(status=discord.Status.dnd,
                                      activity=discord.Activity(name='{}'.format(statuss),
                                                                type=discord.ActivityType.playing))
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_msg**, I chose the default one: **Playing**.",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
        elif a == "playing" or a == "p":
            if len(a) == 1:
                statuss = ctx.message.content[9:]
            elif len(a) == 7:
                statuss = ctx.message.content[15:]
            embed = discord.Embed(description="Status changed. \n**Online**\n**Playing {}**".format(statuss),
                                 color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(statuss),
                                                                type=discord.ActivityType.playing))
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_ttpe**, I chose the default one: **Online**.",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
        elif a == "w" or a == "watching":
            if len(a) == 1:
                statuss = ctx.message.content[9:]
            elif len(a) == 8:
                statuss = ctx.message.content[16:]
            embed = discord.Embed(description="Status changed. \n**Online**\n**Watching {}**".format(statuss),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(statuss),
                                                                type=discord.ActivityType.watching))
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_type**, I chose the default one: **Online**.",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
        elif a == "l" or a == "listening":
            if len(a) == 1:
                statuss = ctx.message.content[9:]
            elif len(a) == 9:
                statuss = ctx.message.content[17:]
            embed = discord.Embed(description="Status changed. \n**Online**\n**Listening to {}**".format(statuss),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(statuss),
                                                                type=discord.ActivityType.listening))
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_type**, I chose the default one: **Online**.",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
        else:
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_type** and/or **status_msg** combination, I chose the default ones: **Online** and **Playing**.",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
            embed = discord.Embed(description="Status changed. \n**Online**\n**Playing {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.playing))

        embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=ctx.message.author.guild.icon_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="You didn't provide a status.", color=0xFF3639)
        embed.set_image(url=ctx.message.author.guild.icon_url)
        embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text="Error raised on: {}".format(ctx.message.content))
        await ctx.send(embed=embed)
        return

@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        if len(ctx.message.content) > 8:
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_type** and/or **status_msg**, I think that the status is empty. I'll get the status by your message. (COULD **NOT BE WORKING PROPERLY**!)",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
            status = ctx.message.content[7:]
            embed = discord.Embed(description="Status changed. \n**Online**\n**Playing {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.playing))
            embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url=ctx.message.author.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You didn't provide a status.", color=0xFF3639)
            embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text="Error raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed)
            return
    if isinstance(error, commands.MissingRequiredArgument):
        if len(ctx.message.content) > 8:
            embed2 = discord.Embed(
                description="Since you didn't provide a valid **status_type** and/or **status_msg**, the status may be broken. (COULD **NOT BE WORKING PROPERLY**!)",
                color=0xf2f542)
            embed2.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed2.set_footer(text="Warning raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed2)
            status = ctx.message.content[7:]
            embed = discord.Embed(description="Status changed. \n**Online**\n**Playing {}**".format(status),
                                  color=0x000000)
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(name='{}'.format(status),
                                                                type=discord.ActivityType.playing))
            embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url=ctx.message.author.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You didn't provide a status.", color=0xFF3639)
            embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text="Error raised on: {}".format(ctx.message.content))
            await ctx.send(embed=embed)
            return
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"**{ctx.message.author.name}** you don't have the **administrator** perms, duh.")
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, None, file=sys.stderr)

bot.load_extension("jishaku")  
bot.run("NzU3Nzk1ODQxMTAzNzU3NDY1.X2lmXw.WSPmuDBRGkvLDWhIQYLuELRYafA")
