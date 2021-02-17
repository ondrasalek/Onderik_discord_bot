import discord
from discord.ext import commands
import json
from random import randint
import validators

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#----------------------------_AUTOROLE_----------------------------
    @commands.command(aliases=["ar"],
					help = "Nastavit automatickou roli.")
    @commands.has_permissions(administrator = True)
    async def autorole(self, ctx, role: discord.Role = None):
        guild = ctx.guild
        roles = guild.roles
        if role is None:
            f = open(f"guilds/{guild.id}.json", "r+") 
            data = json.load(f)
            data["Autorole"] = ""
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()

            embed = discord.Embed(
                        title = "Automatická role byla zrušena.",
                    )
        else:
            color = role.color
            roleId = role.id
            f = open(f"guilds/{guild.id}.json", "r+") 
            data = json.load(f)

            data["Autorole"] = roleId

            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()

            embed = discord.Embed(
                        title = "Automatická role je nastavena jako:",
                        description = role.mention,
                        color = color
                    )
        await ctx.send(embed=embed)
#-------------------------------_URL_--------------------------------
    @commands.command(aliases=["url"],
                    help = "Nastavit url serveru.",
                    description = "!url None ... Zruší URL serveru.")
    @commands.has_permissions(administrator = True)
    async def guild_url(self, ctx, url: str):
        guild = ctx.guild
        if url == "None" or url == "" or url == "none":
            f = open(f"guilds/{guild.id}.json", "r+") 
            data = json.load(f)
            data["URL"] = ""
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()

            embed = discord.Embed(
                        title = "URL nebyl přiřazen.",
                    )
        else:
            valid=validators.url(url)
            if valid == True:
                f = open(f"guilds/{guild.id}.json", "r+") 
                data = json.load(f)
                data["URL"] = url
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()

                embed = discord.Embed(
                            title = "URL k serveru je:",
                            description = url,
                            color = randint(0, 0xffffff)
                        )
            else:
                embed = discord.Embed(
                        title = "Vložený text není URL!",
                    )
        await ctx.send(embed=embed)
#----------------------------_BOTLOG_----------------------------
    @commands.command(aliases=["bl"],
					help = "Nastaví channel BOT LOG",
                    description="")
    @commands.has_permissions(administrator = True)
    async def set_botlog(self, ctx, channel: str):
        guild = ctx.guild
        if channel == "None" or channel == "":
            f = open(f"guilds/{guild.id}.json", "r+") 
            data = json.load(f)
            data["BotLog"] = ""
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()

            embed = discord.Embed(
                        title = "BotLog channel je zrušen.",
                        color = randint(0, 0xffffff)
                    )
        else:
            try:
                if discord.utils.get(guild.channels, name=channel) is not None:
                    bl = discord.utils.get(guild.channels, name=channel)
                elif discord.utils.get(guild.channels, mention=channel) is not None:
                    bl = discord.utils.get(guild.channels, mention=channel)
                elif discord.utils.get(guild.channels, id=int(channel)) is not None:
                    bl = discord.utils.get(guild.channels, id=int(channel))
            
                if discord.ChannelType.text == bl.type:
                    f = open(f"guilds/{guild.id}.json", "r+") 
                    data = json.load(f)
                    data["BotLog"] = bl.id
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
                    f.close()
                    embed = discord.Embed(
                        title = "BotLog channel je nastaven",
                        description = bl.mention,
                        color = randint(0, 0xffffff)
                        )
                else:
                    embed= discord.Embed(
                        title = "Nevybrali jste textový channel",
                        color = discord.Colour.dark_red()
                    )

            except:
                embed= discord.Embed(
                    title = "Tento channel neexistuje!",
                    color = discord.Colour.dark_red()
                    )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Server(bot))