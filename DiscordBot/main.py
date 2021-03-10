#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 21:44:42 2021

@author: osalek
"""
#------------------------------------------------------------------
import discord
from discord.ext import commands
import json

import os
from dotenv import load_dotenv
#------------------------------------------------------------------
#------------------------------------------------------------------
load_dotenv()
token = os.getenv("token")
prefix = os.getenv("prefix")

prefix_help = f"{prefix}command"
#custom_prefix = {}
#------------------------------------------------------------------
# Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=[prefix], intents = intents)
   #TODO: MAKE ADMINS TO CHOOSING PREFIX

#------------------------------------------------------------------
# Load cogs
initial_extensions = [
	"cogs.info",
	"cogs.clear",
	"cogs.server",
	"cogs.onCommandError",
	"cogs.msg_welcome",
 	"cogs.msg_private",
    "cogs.msg_bye",
    "cogs.music",
    "cogs.command"
]
if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception:
			print(f"Failed to load extension {extension}")
   #TODO: MAKE EXTENSIONS TO CHOOSING
#-----------------------_ON_READY_---------------------------------
game = discord.Game(name=f"🤖{prefix_help}🤖")
@bot.event
async def on_ready():
    print(f'{bot.user.name} online 🟢')
    print(f"Discord version: {discord.__version__}")
    await bot.change_presence(activity=game)
	#------------------------------------------------------------------
    guilds = bot.guilds
    for guild in guilds:
        guild_dict = {
					"GuildID": guild.id,
     				"GuildName":guild.name,
					"Autorole": "",
					"URL": "", 
					"BotLog": "",
					"WelcomeMSG": "",
					"PrivateMSG": "",
					"ByeMSG": ""
					}
        try:
            f = open(f"guilds/{guild.id}.json", "r")
        except:
            f = open(f"guilds/{guild.id}.json", "w")
            json.dump(guild_dict, f, indent=4)
        f.close()

@bot.event
async def on_guild_join(ctx):
    guilds = bot.guilds
    for guild in guilds:
        guild_dict = {
					"GuildID": guild.id,
					"GuildName":guild.name,
					"Autorole": "",
					"URL": "", 
					"BotLog": "",
					"WelcomeMSG": "",
					"PrivateMSG": "",
                    "ByeMSG": ""
        			}
        try:
            f = open(f"guilds/{guild.id}.json", "r")
        except:
            f = open(f"guilds/{guild.id}.json", "w")
            json.dump(guild_dict, f, indent=4)
        f.close()
#------------------------------------------------------------------
#------------------------------------------------------------------
bot.run(token)
