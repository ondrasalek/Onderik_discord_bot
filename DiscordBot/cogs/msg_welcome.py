import discord
from discord.ext import commands
import json
#------------------------------------------------------------------
#------------------------------------------------------------------
class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: MAKE SANDING PHOTO
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        
        owner = guild.owner.mention
        icon_url = guild.icon_url
        
        wcolor = 0xfafafa
                
        # autorole
        f = open(f"./DiscordBot/guilds/{guild.id}.json", "r")
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
            wmsg = data["WelcomeMSG"]
            if wmsg == "":
                wmsg = None
            else:
                try:
                    url = data["URL"]
                    if url == "":
                        url = None
                except KeyError:
                    url = None
                    
                wmsg = wmsg.replace("{user}",f"{member.mention}")
                wmsg = wmsg.replace("{server}",f"{guild.name}")
                wmsg = wmsg.replace("{owner}",f"{owner}")
                wmsg = wmsg.replace("{url}",f"{url}")
                
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
                except AttributeError:
                    pass
        except KeyError:
            pass
        f.close()
#------------------------------------------------------------------
def setup(bot):
    bot.add_cog(Welcome(bot))
