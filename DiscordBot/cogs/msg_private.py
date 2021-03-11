import discord
from discord.ext import commands
import json
#------------------------------------------------------------------
#------------------------------------------------------------------
class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        owner = guild.owner.mention
        icon_url = guild.icon_url
        
        pcolor = 0xa4edd1 
        
        f = open(f"./guilds/{guild.id}.json", "r")
        data = json.load(f)
        try:
            pmsg = data["PrivateMSG"]
            if pmsg == "":
                pmsg = None
            else:
                try:
                    url = data["URL"]
                    if url == "":
                        url = None
                except KeyError:
                    url = None
                    
                pmsg = pmsg.replace("{user}",f"{member.mention}")
                pmsg = pmsg.replace("{server}",f"{guild.name}")
                pmsg = pmsg.replace("{owner}",f"{owner}")
                pmsg = pmsg.replace("{url}",f"{url}")
                
                embedPM = discord.Embed(
                    title=url,
                    description=pmsg,
                    color = pcolor
                )
                embedPM.set_author(name=guild.name, icon_url=icon_url)
                
                try:
                    await member.send(embed=embedPM)
                except discord.errors.Forbidden:
                    pass
                except discord.errors.HTTPException:
                    pass
        except KeyError:
            pass
        f.close()
#------------------------------------------------------------------    
def setup(bot):
    bot.add_cog(Private(bot))
