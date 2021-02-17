import discord
from discord.ext import commands
import datetime
import json

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        
        owner = guild.owner.mention
        icon_url = guild.icon_url
        #avatar_url = owner.avatar_url

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
                except Exception:
                    pass
        except Exception:
            pass

        try:
            url = data["URL"]
            if url == "":
                url = None
        except:
            url = None
        f.close()
        
        try:
            #Soukromá zpráva
            embedPM = discord.Embed(
                title=url,
                description=f"Ahoj {member.mention}, na serveru **{guild.name}** si prosím nastav přezdívku tak, ať se poznáme.",
                color = discord.Colour.green()
            )
            embedPM.set_author(name=guild.name, icon_url=icon_url)
            await member.send(embed=embedPM)

            #Vítací zpráva
            embedMSG = discord.Embed(
                #title = f"{guild.name}",
                description = f"Ahoj {member.mention}, vítej na serveru **{guild.name}**!",
                color = discord.Colour.purple()
            )
            embedMSG.set_author(name=guild.name, icon_url=icon_url)
            embedMSG.add_field(name="Abys měl správné role, napiš uživateli:", value=owner, inline=True)
            embedMSG.set_thumbnail(url=icon_url)
        except Exception: 
            #Vítací zpráva
            embedMSG = discord.Embed(
                #title = f"{guild.name}",
                description = f"Ahoj {member.mention}, vítej na serveru **{guild.name}**!",
                color = discord.Colour.purple()
            )
            embedMSG.set_author(name=guild.name, icon_url=icon_url)
            embedMSG.add_field(name="Abys měl správné role, napiš uživateli:", value=owner, inline=True)
            embedMSG.set_footer(text="Nemáš povolené posílání zpráv od uživatelů na serveru, nastav si to prosím.")
            embedMSG.set_thumbnail(url=icon_url)
        try:
            channel = guild.system_channel
            await channel.send(embed=embedMSG)
        except:
            pass

def setup(bot):
    bot.add_cog(Welcome(bot))
