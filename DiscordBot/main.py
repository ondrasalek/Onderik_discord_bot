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
import datetime
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

def get_prefix(bot, message):
    f = open("./guilds/prefixes.json", "r")
    prefixes = json.load(f)
    try:
        return prefixes[str(message.guild.id)]
    except AttributeError:
        pass
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
@bot.event
async def on_ready():
    guilds = bot.guilds
    print(f"{bot.user.name}: online 🟢")
    print(f"> ({len(guilds)}) guilds")
    print(f"Discord version: {discord.__version__}")
        
    #watch = discord.Activity(type=discord.ActivityType.watching, name=f"{len(guilds)}.Servers")
    #listening = discord.Activity(type=discord.ActivityType.listening, name=f"PREFIX {bot.user.name}")
    playing = discord.Activity(type=discord.ActivityType.playing, name=f"PREFIX ONDERIK")
    await bot.change_presence(activity=playing)
	#------------------------------------------------------------------
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
            f = open(f"./guilds/prefixes.json", "r+")
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
            f = open(f"./guilds/prefixes.json", "w")
            prefixes[str(guild.id)] = def_prefix
            json.dump(prefixes, f, indent=4)
        f.close()

@bot.event
async def on_guild_join(guild):
    guilds = bot.guilds
    print(f">{len(guilds)}: guilds (+1) >{guild.name}<")
    
    try:
        f = open(f"./guilds/{guild.id}.json", "r")
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
        f = open(f"./guilds/prefixes.json", "r+")
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
        f = open(f"./guilds/prefixes.json", "w")
        prefixes[str(guild.id)] = def_prefix
        json.dump(prefixes, f, indent=4)
    f.close()
    try:
        name = bot.user.name
        text = f"""
        **-** Prefix je **`{def_prefix}`**
        **-** List příkazů zobrazíte příkazem `{def_prefix}command`
        **-** Prefix si nastavíte pomocí `{def_prefix}change_prefix`
        **-** Více se dočtete na:
        **https://ondrasalek.github.io/onderik/**
        **-** Pokud potřebujete pomoc, přidejte se na Server Podpory:
        **https://discord.gg/bHMn2FSga7**
        
        Příkazem `PODPORA {str(name)}` pošlete pozvánku na Server Podpory
        Příkazem `PREFIX {str(name)}` zobrazíte nastavený prefix
        """
        
        embed = discord.Embed(
            title = f"Děkuji za pozvání 🥰",
            description = text,
            timestamp=datetime.datetime.utcnow(),
            color = 0x32a852
        )
        channel = guild.system_channel
        await channel.send(embed=embed)
    except AttributeError:
        pass
    except discord.errors.Forbidden:
        pass
    
@bot.event
async def on_guild_remove(guild):
    guilds = bot.guilds
    print(f">{len(guilds)}: guilds (-1) >{guild.name}<")
    
    if os.path.exists(f"./guilds/{guild.id}.json"):
        os.remove(f"./guilds/{guild.id}.json")
        
    try:
        f = open(f"./guilds/prefixes.json", "r+")
        prefixes = json.load(f)
        if str(guild.id) in prefixes:
            prefixes.pop(str(guild.id))
            f.seek(0)
            json.dump(prefixes, f, indent=4)
            f.truncate()
    except:
        prefixes = {}
        f = open(f"./guilds/prefixes.json", "w")
        prefixes[str(guild.id)] = def_prefix
        json.dump(prefixes, f, indent=4)
    f.close()
#------------------------------------------------------------------
#------------------------------------------------------------------
bot.run(token)
