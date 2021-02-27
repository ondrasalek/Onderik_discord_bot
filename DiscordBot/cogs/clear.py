import discord
from discord.ext import commands
import time
import datetime
import json
#------------------------------------------------------------------
#------------------------------------------------------------------
class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cl','smazat'],
					help = "Vymazat zprávy (max 333).")
					
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount > 333:
            amount = 333
            await ctx.send("```Maximálně lze smazat 333 zpráv\nBudou smazány za 5 sekund!```")
            time.sleep(5)

        guild = ctx.guild

        author = ctx.author
        TChannel = ctx.channel
        await ctx.channel.purge(limit=amount)
        

        embed1 = discord.Embed(
                timestamp = datetime.datetime.utcnow(),
                color = discord.Colour.dark_red()
            )
        embed1.add_field(name=f'Smazání {amount} zpráv uživatelem', value=author.mention,inline=False)

        embed2 = discord.Embed(
                timestamp = datetime.datetime.utcnow(),
                color = discord.Colour.dark_red()
            )
        embed2.add_field(name=f"Smazání {amount} zpráv v", value=TChannel.mention,inline=False)
        embed2.add_field(name='uživatelem', value=author.mention,inline=False)
        
        f = open(f"guilds/{guild.id}.json", "r")
        data = json.load(f)
        try:
            channel = data["BotLog"]
            if channel == "":
                await ctx.send(embed=embed1)
            else:
                channel = discord.utils.get(guild.channels, id=channel)
                if channel == TChannel:
                    await ctx.send(embed=embed1)
                elif channel != TChannel:
                    await channel.send(embed=embed2)
                    await ctx.send(embed=embed1)
        except:
            await ctx.send(embed=embed1)

        f.close()
#------------------------------------------------------------------
def setup(bot):
    bot.add_cog(Clear(bot))