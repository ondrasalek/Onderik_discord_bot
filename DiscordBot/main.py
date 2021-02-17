#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 21:44:42 2021

@author: osalek
"""
#------------------------------------------------------------------
import discord
from discord.ext import commands,tasks
import json
from itertools import cycle
#------------------------------------------------------------------
#------------------------------------------------------------------
# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	
prikaz = f"{prefix}help"
#------------------------------------------------------------------
# Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=[prefix], intents = intents)
#------------------------------------------------------------------
# Load cogs
initial_extensions = [
	"clear",
	"server",
	"info",
	"onCommandError",
	"welcome"
]
if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(f"Failed to load extension {extension}")
#-----------------------_ON_READY_---------------------------------
@bot.event
async def on_ready():
    change_status.start()
    print(f'{bot.user.name} online 🟢')
    print(f"Discord verze: {discord.__version__}")

#------------------------------------------------------------------
    guilds = bot.guilds
    for guild in guilds:
        guild_dict = {
					"GuildID":guild.id
					}
        try:
            f = open(f"guilds/{guild.id}.json", "r")
            data = json.load(f)
        except:
            f = open(f"guilds/{guild.id}.json", "w")
            json.dump(guild_dict, f)
        f.close()
#-----------------------_ACTIVITY_---------------------------------
status = cycle([prikaz,"🔴LIVE",prikaz,"🤖BOT",prikaz,"🟢author: ONDER"])
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))
#------------------------------------------------------------------
#------------------------------------------------------------------
bot.run(token)