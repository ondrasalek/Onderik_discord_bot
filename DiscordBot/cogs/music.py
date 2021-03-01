import asyncio

import discord
import youtube_dl

from discord.ext import commands
#------------------------------------------------------------------
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
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
                      help="PLAY YouTube")
    async def play(self, ctx, *, url):
        if url.find("open.spotify.com") != -1:
            embed= discord.Embed(
                    title = "Podporovaný formát URL je pouze pro YouTube",
                    color = discord.Colour.dark_red()
                )
            await ctx.send(embed=embed)
        else:
            global this
            global text_channel
            global voice_channel
            
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
        
            this = str(f"""**```fix\n{player.title}```**""")
            
            embed = discord.Embed(
                        color = 0xFF1493
                    )
            embed.add_field(name=f"Právě hraje",value=this,inline=False)
            embed.add_field(name="\u200b",value=f"🔊🎶`{ctx.author.voice.channel}`",inline=False)
            await ctx.send(embed=embed)
            
            text_channel = ctx.channel
            voice_channel = ctx
        
    @commands.command(aliases = ["pozastavit"],
                      help = "PAUSE")   
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            embed = discord.Embed(
                        title = "Pause",
                        description = this,
                        color = 0xFF1493
                    )
            embed.add_field(name="\u200b",value=f"⏸`{ctx.author.voice.channel}`",inline=False)
            await ctx.send(embed=embed)
            await ctx.voice_client.pause()
        else:
            embed= discord.Embed(
                    title = "BOT nehraje.",
                    color = 0xFF1493
                )
            await ctx.send(embed=embed)

    @commands.command(aliases=["continue","pokracuj"],
                      help="RESUME")   
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            embed = discord.Embed(
                        title = "Resume",
                        description = this,
                        color = 0xFF1493
                    )
            embed.add_field(name="\u200b",value=f"⏯`{ctx.author.voice.channel}`",inline=False)
            await ctx.send(embed=embed)
            await ctx.voice_client.resume()
        else:
            embed = discord.Embed(
                    title = "BOT není pozastaven.",
                    color = 0xFF1493
                )
            await ctx.send(embed=embed)
            
    @commands.command(help="STOP")
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            embed = discord.Embed(
                        title = "🔇Stop & Disconnect",
                        color = 0xFF1493
                    )
            await ctx.send(embed=embed)
            await ctx.voice_client.disconnect()
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global this
        global text_channel
        global voice_channel
        if this != None and text_channel != None and voice_channel != None:
            if after.channel is not None:
                channel = self.bot.get_channel(after.channel.id)
                count = len(channel.members) - 1
                if count == 0:
                    
                    embed = discord.Embed(
                            title = "🔇Stop & Disconnect",
                            color = 0xFF1493
                        )
                    await text_channel.send(embed=embed)
                    await voice_channel.voice_client.disconnect()
                    this = None
                    text_channel = None
                    voice_channel = None

this = None
text_channel = None
voice_channel = None
#------------------------------------------------------------------
def setup(bot):
    bot.add_cog(Music(bot))
