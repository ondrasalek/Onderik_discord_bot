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
					help = "Nastavit automatickou roli.",
                    description="""
                                * [autorole] ... Zruší automatické role *
                                """
                    )
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
                        color = randint(0, 0xffffff)
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
                    description="""
                                * [url] "None" ... Zruší URL *
                                * [url] "url" ... zobrazí aktuální URL *
                                """
                    )
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
                        title = "URL je __zrušeno__.",
                        color = randint(0, 0xffffff)
                    )
        else:
            if url == "url" or url == "now":
                f = open(f"guilds/{guild.id}.json", "r")
                data = json.load(f)
                try:
                    url = data["URL"]
                    if url == "":
                        url = None
                except:
                    url = None
                f.close() 
                
                embed = discord.Embed(
                    title = "AKTUÁLNĚ",
                    description = url,
                    color = discord.Colour.gold()
                    )
            else:
                if len(url)<2048:
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
                                color = discord.Colour.dark_red()

                            )
                else:
                    embed= discord.Embed(
                                title = "URL adresa je moc dlouhá.",
                                description = f"{len(url)} znaků!",
                                color = discord.Colour.dark_red()
                                )
        await ctx.send(embed=embed)
#----------------------------_BOTLOG_----------------------------
    @commands.command(aliases=["bl"],
					help = "Nastaví channel BOT LOG",
                    description="""
                                * [set_botlog] "None" ... Zruší aktuální botlog channel *
                                * [set_botlog] "channel" ... zobrazí aktuální botlog channel *
                                """
                    )
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
                        title = "BotLog channel je __zrušen__.",
                        color = randint(0, 0xffffff)
                    )
        else:
            if channel == "channel" or channel == "now":
                f = open(f"guilds/{guild.id}.json", "r")
                data = json.load(f)
                try:
                    botlog = data["BotLog"]
                    if botlog == "":
                        botlog = None
                    else:
                        botlog = discord.utils.get(guild.channels, id=botlog)
                        botlog=botlog.mention
                except:
                    botlog = None
                f.close() 
                
                embed = discord.Embed(
                    title = "AKTUÁLNĚ",
                    color = discord.Colour.gold()
                    )
                embed.add_field(name='BotLog Channel', value=botlog, inline=False)
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
#----------------------------_WELCOME_----------------------------
    @commands.command(aliases=["wmsg"],
					help = "Nastavit Welcome zprávu (max 255 znaků).",
                    description="""
                                Můžete použít:
                                Member ... {user}
                                Server ... {server}
                                Owner ... {owner}
                                Url ... {url}
                                
                                * [welcome_message] "message" ... zobrazí aktuální zprávu *
                                """
                    )
    @commands.has_permissions(administrator = True)
    async def welcome_message(self, ctx, message: str):
        guild = ctx.guild
        author = ctx.author
        owner = guild.owner.mention

        if message == "None" or message == "" or message == "default":
            wm = "Ahoj {user}, vítej na serveru **{server}**!"
            
            f = open(f"guilds/{guild.id}.json", "r+") 
            data = json.load(f)
            data["WelcomeMSG"] = wm
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()
            
            embed = discord.Embed(
                        color = randint(0, 0xffffff)
                    )
            embed.add_field(name="Welcome zpráva je nastavena na __základní__:", value=wm, inline=False)
            await ctx.send(embed=embed)

        else:
            if message == "message" or message == "now":
                f = open(f"guilds/{guild.id}.json", "r")
                data = json.load(f)
                message = data["WelcomeMSG"]
                    
                try:
                    url = data["URL"]
                    if url == "":
                        url = None
                except:
                    url = None
                f.close() 
                message = message.replace("{user}",f"{author.mention}")
                message = message.replace("{server}",f"{guild.name}")
                message = message.replace("{owner}",f"{owner}")
                message = message.replace("{url}",f"{url}")
                
                icon_url = guild.icon_url

                embed = discord.Embed(
                    title = "AKTUÁLNĚ",
                    color = discord.Colour.gold()
                    )
                await ctx.send(embed=embed)
                
                embedW = discord.Embed(
                    description = message,
                    color = discord.Colour.gold()
                    )
                embedW.set_author(name=guild.name, icon_url=icon_url)
                embedW.set_thumbnail(url=icon_url)

                await ctx.send(embed=embedW)
            else:
                if len(message) < 333:
                    f = open(f"guilds/{guild.id}.json", "r+") 
                    data = json.load(f)
                    data["WelcomeMSG"] = message
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
                    
                    try:
                        url = data["URL"]
                        if url == "":
                            url = None
                    except:
                        url = None
                    f.close()
                    
                    embed = discord.Embed(
                                color = randint(0, 0xffffff)
                            )
                    embed.add_field(name="Welcome zpráva je nastavena na:", value=message, inline=False)
                    embed.add_field(name="--->>>", value="**Zpráva bude vypadat následovně.**", inline=False)
                    await ctx.send(embed=embed)
                    
                    message = message.replace("{user}",f"{author.mention}")
                    message = message.replace("{server}",f"{guild.name}")
                    message = message.replace("{owner}",f"{owner}")
                    message = message.replace("{url}",f"{url}")
                    
                    icon_url = guild.icon_url

                    embedW = discord.Embed(
                        description = message,
                        color = discord.Colour.purple()
                        )
                    embedW.set_author(name=guild.name, icon_url=icon_url)
                    embedW.set_thumbnail(url=icon_url)

                    await ctx.send(embed=embedW)
                else:
                    embed= discord.Embed(
                            title = "Zpráva je moc dlouhá.",
                            description = f"{len(message)} znaků!",
                            color = discord.Colour.dark_red()
                            )
                    await ctx.send(embed=embed)
#----------------------------_PRIVATE_----------------------------
    @commands.command(aliases=["pmsg"],
					help = "Nastavit Privátní welcome zprávu (max 255 znaků).",
                    description="""
                                Můžete použít:
                                Member ... {user}
                                Server ... {server}
                                Owner ... {owner}
                                Url ... {url}
                                
                                * [private_w_message] "message" ... zobrazí aktuální zprávu *
                                """
                    )
    @commands.has_permissions(administrator = True)
    async def private_w_message(self, ctx, message: str):
        guild = ctx.guild
        author = ctx.author
        owner = guild.owner.mention

        if message == "None" or message == "" or message == "default":
            pm = None
            f = open(f"guilds/{guild.id}.json", "r+") 
            data = json.load(f)
            data["PrivateMSG"] = ""
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()
            
            embed = discord.Embed(
                        color = randint(0, 0xffffff)
                    )
            embed.add_field(name="Private welcome zpráva je __zrušena__:", value=pm, inline=False)
            await ctx.send(embed=embed)

        else:
            if message == "message" or message == "now":
                f = open(f"guilds/{guild.id}.json", "r")
                data = json.load(f)
                try:
                    url = data["URL"]
                    if url == "":
                        url = None
                except:
                    url = None
                    
                try:
                    message = data["PrivateMSG"]
                    if message == "":
                        message = "Nothing"
                        embed = discord.Embed(
                            title = "AKTUÁLNĚ",
                            description = message,
                            color = discord.Colour.gold()
                            )
                        await ctx.send(embed=embed)
                    else:
                        message = message.replace("{user}",f"{author.mention}")
                        message = message.replace("{server}",f"{guild.name}")
                        message = message.replace("{owner}",f"{owner}")
                        message = message.replace("{url}",f"{url}")
                        
                        icon_url = guild.icon_url

                        embed = discord.Embed(
                            title = "AKTUÁLNĚ",
                            color = discord.Colour.gold()
                            )
                        await ctx.send(embed=embed)
                        
                        embedW = discord.Embed(
                            description = message,
                            color = discord.Colour.gold()
                            )
                        embedW.set_author(name=guild.name, icon_url=icon_url)

                        await ctx.send(embed=embedW)
                        
                except:
                    message = "Nothing"
                    embed = discord.Embed(
                            title = "AKTUÁLNĚ",
                            description = message,
                            color = discord.Colour.gold()
                            )
                    await ctx.send(embed=embed)
                f.close() 
                
            else:
                if len(message) < 333:
                    f = open(f"guilds/{guild.id}.json", "r+") 
                    data = json.load(f)
                    data["PrivateMSG"] = message
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
                    
                    try:
                        url = data["URL"]
                        if url == "":
                            url = None
                    except:
                        url = None
                    f.close()
                    
                    embed = discord.Embed(
                                color = randint(0, 0xffffff)
                            )
                    embed.add_field(name="Private welcome zpráva je nastavena na:", value=message, inline=False)
                    embed.add_field(name="--->>>", value="**Zpráva bude vypadat následovně.**", inline=False)
                    await ctx.send(embed=embed)
                    
                    message = message.replace("{user}",f"{author.mention}")
                    message = message.replace("{server}",f"{guild.name}")
                    message = message.replace("{owner}",f"{owner}")
                    message = message.replace("{url}",f"{url}")
                    
                    icon_url = guild.icon_url

                    embedW = discord.Embed(
                        description = message,
                        color = discord.Colour.purple()
                        )
                    embedW.set_author(name=guild.name, icon_url=icon_url)

                    await ctx.send(embed=embedW)
                else:
                    embed= discord.Embed(
                            title = "Zpráva je moc dlouhá.",
                            description = f"{len(message)} znaků!",
                            color = discord.Colour.dark_red()
                            )
                    await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Server(bot))