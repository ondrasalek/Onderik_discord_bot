import discord
from discord.ext import commands

class OnCommandErrorCog(commands.Cog, name="on command error"):
	def __init__(self, bot):
		self.bot = bot
        
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			embed = discord.Embed(
				title = 'ERROR',
				description='Neznámý příkaz!',
				color = discord.Colour.dark_red()
			)
			embed.add_field(name='Zkuste:', value='!help')
			await ctx.send(embed=embed)
		elif isinstance(error, commands.MissingPermissions):
				embed= discord.Embed(
					title = "Nedostatečné pravomoce!",
					color = discord.Colour.dark_red()
				)
				await ctx.send(embed=embed)
		elif isinstance(error, commands.BadArgument):
				embed= discord.Embed(
					title = "Chyba v argumentu!",
					color = discord.Colour.dark_red()
					)
				await ctx.send(embed=embed)
		elif isinstance(error, commands.MissingRequiredArgument):
				embed= discord.Embed(
					title = "Chybí argument!",
					color = discord.Colour.dark_red()
				)
				await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(OnCommandErrorCog(bot))