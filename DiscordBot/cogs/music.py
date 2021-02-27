import asyncio

import discord
import youtube_dl
import math

from discord.ext import commands
#------------------------------------------------------------------
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "options": "-vn",
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
#------------------------------------------------------------------
#------------------------------------------------------------------
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["p"],
                      help="PLAY music.")
    async def play(self, ctx, *, url):
        global this
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect() #connect to channel
            else:
                embed= discord.Embed(
					title = "Nejste připojeni v voice channelu.",
					color = discord.Colour.dark_red()
				)
                await ctx.send(embed=embed)
        elif ctx.voice_client.is_playing(): # is connected to channel & stop
            ctx.voice_client.stop()
            
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            
        this = str(f"""```fix\n{player.title}```""")
        
        embed = discord.Embed(
					title = "Právě hraje:",
                    description = this,
					color = 0xFF1493
				)
        message = await ctx.send(embed=embed)
        await message.add_reaction("🟢")
        
    @commands.command(aliases = ["pozastavit"],
                      help = "PAUSE music.")   
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            embed = discord.Embed(
                        title = f"Pause",
                        description = this,
                        color = 0xFF1493
                    )
            message = await ctx.send(embed=embed)
            await message.add_reaction("⏸")
            await ctx.voice_client.pause()
        else:
            embed= discord.Embed(
					title = "BOT nehraje.",
					color = 0xFF1493
				)
            await ctx.send(embed=embed)
        
    @commands.command(aliases=["continue","pokracuj"],
                      help="RESUME music.")   
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            embed = discord.Embed(
                        title = f"Resume",
                        description = this,
                        color = 0xFF1493
                    )
            message = await ctx.send(embed=embed)
            await message.add_reaction("▶")
            await ctx.voice_client.resume()
        else:
            embed = discord.Embed(
					title = "BOT není pozastaven.",
					color = 0xFF1493
				)
            await ctx.send(embed=embed)
        
    @commands.command(help="STOP music.")
    async def stop(self, ctx):
        embed = discord.Embed(
                    title = f"Stop.",
                    color = 0xFF1493
                )
        message = await ctx.send(embed=embed)
        await message.add_reaction("🔴")
        await ctx.voice_client.disconnect()

this = ""
#------------------------------------------------------------------
def setup(bot):
    bot.add_cog(Music(bot))