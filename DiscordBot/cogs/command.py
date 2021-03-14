import discord
from discord.ext import commands
import json

class HelpCog(commands.Cog, name="Zavolá tuto POMOC"):
	def __init__(self, bot):
		self.bot = bot
  
	@commands.command(usage = "(název commandu)",
                    help = "Seznam příkazů",
					description = "Zobrazí nápovědu.",
                    hidden = True)
	async def command (self, ctx, commandName=None):
            with open("./configuration.json", "r") as config: 
                data = json.load(config)
                prefix = data["prefix"]
            if commandName is None:
                embed = discord.Embed(
                            #title = f"__{self.bot.user.name}__ HELP", 
                            title = "**List všech příkazů**",
                            url="https://discord.gg/bHMn2FSga7",
                            color = 0x66ffcc
                        )
                for cog in self.bot.cogs:
                    cog1 = True
                    for command in self.bot.commands:
                        if cog == command.cog_name:
                            if cog1 is True:
                                embed.add_field(name="\u200b",value=f"**```fix\n{cog}```**",inline=False)
                                cog1 = False
                            embed.add_field(name="\u200b", value=f"**`{prefix}{command.name}`** | {command.help}", inline=True)
                await ctx.send(embed=embed)
            else:
                for cmd in self.bot.commands:
                    if commandName == cmd.name:
                        embed = discord.Embed(
                                title = f"`{prefix}{cmd.name}`",
                                description=f"{cmd.aliases}\n*{cmd.help}*\n\n{cmd.description}",
                                color = 0x66ffcc
                            )
                        #embed.add_field(name="asdasd",value=cmd.clean_params)
                        return await ctx.send(embed=embed)
                if commandName != cmd.name:
                    embed = discord.Embed(
                                title = 'ERROR',
                                description='Neznámý příkaz!',
                                color = discord.Colour.dark_red()
                            )
                    await ctx.send(embed=embed)
                        
def setup(bot):
	bot.add_cog(HelpCog(bot))