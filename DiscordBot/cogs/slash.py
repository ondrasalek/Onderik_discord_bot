import discord
from discord.ext import commands
import json

from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext


class SlashCog(commands.Cog, name="Slash"):
    def __init__(self, bot):
        self.bot = bot
    
    #slash = SlashCommand(bot, auto_register=True)

def setup(bot):
    bot.add_cog(SlashCog(bot))
