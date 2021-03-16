#------------------------------------------------------------------
import discord
from discord.ext import commands,tasks
import json
import os
import datetime
#------------------------------------------------------------------
class Schedule(commands.Cog, name="Schedule"):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=60.0)
    async def task(self):
        if datetime.now().hour == 15:
            # Do something
            pass
        
def setup(bot):
    bot.add_cog(Schedule(bot))