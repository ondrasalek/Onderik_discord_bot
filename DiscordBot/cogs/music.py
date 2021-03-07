import asyncio
import validators
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
    'outtmpl': '%(title)s.%(ext)s',
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
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
#------------------------------------------------------------------
#------------------------------------------------------------------
class Music(commands.Cog, name="Music příkazy"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["p"],
                      help="PLAY YouTube")
    async def play(self, ctx, *, url):
        if validators.url(url) and (url.find("https://www.youtube.com/") + url.find("https://youtu.be/")) < -1:
            embed= discord.Embed(
                        title = "Podporovaný formát URL je pouze pro YouTube",
                        color = discord.Colour.dark_red()
                    )
            await ctx.send(embed=embed)
        else:
            if ctx.voice_client is None:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect() #connect to channel
                    if ctx.voice_client.is_playing(): # is connected to channel & stop
                        ctx.voice_client.stop()
                        
                    global this
                    global text_channel
                    
                    async with ctx.typing():
                        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True) #just stream
                        #player = await YTDLSource.from_url(url, loop=self.bot.loop) #download
                        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                
                        this = str(f"""**```fix\n{player.title}```**""")
                        
                        embed = discord.Embed(color = 0xFF1493)
                        embed.add_field(name=f"Právě hraje",value=this,inline=False)
                        embed.add_field(name="\u200b",value=f"🔊🎶`{ctx.author.voice.channel}`",inline=False)
                        await ctx.send(embed=embed)
                        
                        text_channel = ctx.channel
                else:
                    embed= discord.Embed(
                        title = "Nejste připojeni v voice channelu.",
                        color = discord.Colour.dark_red()
                    )
                    await ctx.send(embed=embed)
        # TODO: add to queue
        
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
        if ctx.guild.voice_client.is_playing():
            embed = discord.Embed(
                        title = "🔇Stop",
                        color = 0xFF1493
                    )
            await ctx.send(embed=embed)
            await ctx.guild.voice_client.stop()
            
    @commands.command(aliases=["hlasitost"])
    async def volume(self, ctx, volume: int):
        if ctx.guild.voice_client.is_playing():
            embed = discord.Embed(
                title=f"Hlasitost {volume}%",
                            color = 0xFF1493
                        )
            await ctx.send(embed=embed)
            ctx.voice_client.source.volume = volume / 100
        elif  ctx.guild.voice_client.is_paused():
            embed = discord.Embed(
                    title=f"Hlasitost {volume}%",
                    description = "⏯ BOT je pozastaven",
                    color = 0xFF1493
                )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                    title = "BOT nehraje",
                    color = 0xFF1493
                )
            await ctx.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_state = member.guild.voice_client
        if voice_state is not None and len(voice_state.channel.members) == 1:
            embed = discord.Embed(
                            title = "🔇Stop & Disconnect",
                            color = 0xFF1493
                        )
            await text_channel.send(embed=embed)
            await voice_state.disconnect()
        elif voice_state is not None:
            await asyncio.sleep(30) #wait 30 seconds
            try:
                asyncio.run_coroutine_threadsafe(voice_state.disconnect(), self.bot.loop)
                voice_state = None
                embed = discord.Embed(
                                title = "🔇Disconnect",
                                description = "Není co hrát",
                                color = 0xFF1493
                        )
                asyncio.run_coroutine_threadsafe(text_channel.send(embed=embed),self.bot.loop)
            except AttributeError:
                pass
    @commands.command(help="DISCONNECT")
    async def leave(self, ctx):
        if ctx.guild.voice_client.is_connected():
            embed = discord.Embed(
                            title = "🔇Disconnect",
                            color = 0xFF1493
                        )
            await text_channel.send(embed=embed)
            await ctx.guild.voice_client.disconnect()
            
    @commands.command(aliases=["ted"],
                      help="Teď hraje")
    async def now(self, ctx):
        if ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused():
            embed = discord.Embed(color = 0xFF1493)
            embed.add_field(name=f"Právě hraje",value=this,inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                    title = "BOT nehraje",
                    color = 0xFF1493
                )
            await ctx.send(embed=embed)
    # TODO: add fce "skip" & "queue"
    
this = None
text_channel = None
song_queue = []
#------------------------------------------------------------------
def setup(bot):
    bot.add_cog(Music(bot))
