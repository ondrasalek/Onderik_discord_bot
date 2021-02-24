import discord
from discord.ext import commands
import json
#------------------------------------------------------------------
#------------------------------------------------------------------
class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        
        owner = guild.owner.mention
        icon_url = guild.icon_url

        # autorole
        f = open(f"guilds/{guild.id}.json", "r")
        data = json.load(f)
        try:
            autorole = data["Autorole"]
            if autorole == "":
                autorole = None
            else:
                autorole = discord.utils.get(guild.roles, id=autorole)
                try:     
                    await member.add_roles(autorole)
                except:
                    pass
        except KeyError:
            pass

        try:
            url = data["URL"]
            if url == "":
                url = None
        except KeyError:
            url = None
            
        try:
            wmsg = data["WelcomeMSG"]
        except KeyError:
            wmsg = "Ahoj {user}, vítej na serveru **{server}**!"

        try:
            pmsg = data["PrivateMSG"]
            if pmsg == "":
                pmsg = None
            else:
                pmsg = pmsg.replace("{user}",f"{member.mention}")
                pmsg = pmsg.replace("{server}",f"{guild.name}")
                pmsg = pmsg.replace("{owner}",f"{owner}")
                pmsg = pmsg.replace("{url}",f"{url}")
        except KeyError:
            pmsg = None
        f.close()
        
        wmsg = wmsg.replace("{user}",f"{member.mention}")
        wmsg = wmsg.replace("{server}",f"{guild.name}")
        wmsg = wmsg.replace("{owner}",f"{owner}")
        wmsg = wmsg.replace("{url}",f"{url}")
        
        wcolor = 0xfafafa
        pcolor = 0xa4edd1
        try:
            if pmsg is not None:
                #Soukromá zpráva
                embedPM = discord.Embed(
                    title=url,
                    description=pmsg,
                    color = pcolor
                )
                embedPM.set_author(name=guild.name, icon_url=icon_url)
                await member.send(embed=embedPM)
                
            #Vítací zpráva
            embedMSG = discord.Embed(
                #title = f"{guild.name}",
                description = wmsg,
                color = wcolor
            )
            embedMSG.set_author(name=guild.name, icon_url=icon_url)
            embedMSG.set_thumbnail(url=icon_url)

        except: 
            #Vítací zpráva
            embedMSG = discord.Embed(
                #title = f"{guild.name}",
                description = wmsg,
                color = wcolor
            )
            embedMSG.set_author(name=guild.name, icon_url=icon_url)
            embedMSG.set_thumbnail(url=icon_url)
        try:
            channel = guild.system_channel
            await channel.send(embed=embedMSG)
        except:
            pass
        
def setup(bot):
    bot.add_cog(Welcome(bot))
