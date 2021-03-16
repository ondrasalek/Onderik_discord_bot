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
#------------------------------------------------------------------
#------------------------------------------------------------------
'''from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
prefix = os.getenv("prefix")'''

with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	def_prefix = data["prefix"]

prefix_help = f"{def_prefix}command"

def get_prefix(bot, message):
    f = open("./prefixes.json", "r")
    prefixes = json.load(f)
    return prefixes[str(message.guild.id)]
#------------------------------------------------------------------
# Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=(get_prefix), intents = intents)
   #TODO: MAKE ADMINS TO CHOOSE PREFIX

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
    "cogs.command"
    #"cogs.music",
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
    #await bot.change_presence(activity=game)
	#------------------------------------------------------------------
    guilds = bot.guilds
    for guild in guilds:
        try:
            f = open(f"./guilds/{guild.id}.json", "r+")
            data = json.load(f)
            if  data["GuildName"] == guild.name:
                pass
            else:
                data["GuildName"] = guild.name
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except:
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
            f = open(f"./guilds/{guild.id}.json", "w")
            json.dump(guild_dict, f, indent=4)
        f.close()
        try:
            f = open(f"./prefixes.json", "r+")
            prefixes = json.load(f)
            if str(guild.id) in prefixes:
                pass
            else:
                prefixes[str(guild.id)] = def_prefix
                f.seek(0)
                json.dump(prefixes, f, indent=4)
                f.truncate()
        except:
            prefixes = {}
            f = open(f"./prefixes.json", "w")
            prefixes[str(guild.id)] = def_prefix
            json.dump(prefixes, f, indent=4)
        f.close()
   
@bot.event
async def on_guild_join(guild):
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
        f = open(f"./guilds/{guild.id}.json", "r")
    except:
        f = open(f"./guilds/{guild.id}.json", "w")
        json.dump(guild_dict, f, indent=4)
    f.close()
    
    try:
        f = open(f"./prefixes.json", "r+")
        prefixes = json.load(f)
        if str(guild.id) in prefixes:
            pass
        else:
            prefixes[str(guild.id)] = def_prefix
            f.seek(0)
            json.dump(prefixes, f, indent=4)
            f.truncate()
    except:
        prefixes = {}
        f = open(f"./prefixes.json", "w")
        prefixes[str(guild.id)] = def_prefix
        json.dump(prefixes, f, indent=4)
    f.close()

@bot.event
async def on_guild_remove(guild):
    if os.path.exists(f"./guilds/{guild.id}.json"):
        os.remove(f"./guilds/{guild.id}.json")
        
    try:
        f = open(f"./prefixes.json", "r+")
        prefixes = json.load(f)
        if str(guild.id) in prefixes:
            prefixes.pop(str(guild.id))
            f.seek(0)
            json.dump(prefixes, f, indent=4)
            f.truncate()
    except:
        prefixes = {}
        f = open(f"./prefixes.json", "w")
        prefixes[str(guild.id)] = def_prefix
        json.dump(prefixes, f, indent=4)
    f.close()
#------------------------------------------------------------------
#------------------------------------------------------------------
bot.run(token)
