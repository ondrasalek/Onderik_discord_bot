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
	"cogs.clear",
	"cogs.server",
	"cogs.info",
	"cogs.onCommandError",
	"cogs.msg_welcome",
    "cogs.msg_bye",
    "cogs.music"
]
if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception:
			print(f"Failed to load extension {extension}")
#-----------------------_ON_READY_---------------------------------
game = discord.Game(name=f"🤖{prikaz}🤖")
@bot.event
async def on_ready():
    print(f'{bot.user.name} online 🟢')
    print(f"Discord verze: {discord.__version__}")
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
					"WelcomeMSG": "Ahoj {user}, vítej na serveru **{server}**!",
					"PrivateMSG": "",
					"ByeMSG": ""
					}

        try:
            f = open(f"guilds/{guild.id}.json", "r+")
            data = json.load(f)
            data["GuildName"] = guild.name
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
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
					"WelcomeMSG": "Ahoj {user}, vítej na serveru **{server}**!",
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
