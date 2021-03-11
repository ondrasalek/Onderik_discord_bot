import discord
from discord.ext import commands
import json
#------------------------------------------------------------------
#------------------------------------------------------------------
class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        
        owner = guild.owner.mention
        icon_url = guild.icon_url

        # autorole
        f = open(f"./guilds/{guild.id}.json", "r")
        data = json.load(f)
        bcolor = 0x000000
        try:
            bmsg = data["ByeMSG"]
            if bmsg == "":
                bmsg = None
            else:
                try:
                    url = data["URL"]
                    if url == "":
                        url = None
                except KeyError:
                    url = None
                    
                bmsg = bmsg.replace("{user}",f"{member.display_name}")
                bmsg = bmsg.replace("{server}",f"{guild.name}")
                bmsg = bmsg.replace("{owner}",f"{owner}")
                bmsg = bmsg.replace("{url}",f"{url}")

                embed = discord.Embed(
                    description = bmsg,
                    color = bcolor
                )
                embed.set_author(name=guild.name, icon_url=icon_url)
                try:
                    channel = guild.system_channel
                    await channel.send(embed=embed)
                except AttributeError:
                    pass
        except KeyError:
            pass
        f.close()
#------------------------------------------------------------------    
def setup(bot):
    bot.add_cog(Welcome(bot))
