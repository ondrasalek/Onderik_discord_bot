import discord
from discord.ext import commands
import datetime
from random import randint
import json

url_bot="https://discord.com/api/oauth2/authorize?client_id=804733813976203284&permissions=8&scope=bot"

class Info(commands.Cog, name="Info příkazy"):
    def __init__(self, bot):
        self.bot = bot

#----------------------------_BOT_INFO_----------------------------
    @commands.command(aliases=['i','info',"bot"],
                     help='Info o BOTu.')
    async def info_bot(self, ctx):
        guild = ctx.guild

        f = open("./configuration.json", "r")
        data = json.load(f)
        prefix = data["prefix"]
        f.close()
        prikaz = f"{prefix}command"

        bot = self.bot
        b_bot = bot.user
        
        name = b_bot.name
        nick = b_bot.display_name
        avatar_url = b_bot.avatar_url
        created = b_bot.created_at.__format__('%d.%m. %Y')
        author = ctx.author.display_name

        embed = discord.Embed(
            title=nick,
            url=url_bot,
            timestamp=datetime.datetime.utcnow(),
            color = discord.Colour.dark_blue()
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Vznikl", value=created, inline=True)
        embed.add_field(name="Nabídka příkazů", value=prikaz, inline=True)

        guilds = len(self.bot.guilds)
        text = str(f"""```json\nJsem na {guilds} serverech.```""")
        embed.add_field(name = "Na kolika serverech jsem?", value=text, inline=False)
        
        embed.add_field(name = "\u200b", value=f"__Chceš mě na svůj server?\nNapiš:__ *`ADD {name}`*", inline=True)
        embed.add_field(name = "\u200b", value=f"__Chceš vědět, co budu umět?\nNapiš:__ *`SHOW {name}`*", inline=True)
        
        embed.set_footer(text = f"Zavolal: {author}")
        
        await ctx.send(embed=embed)
        
    # ON MESSAGE "ADD BOT NAME" SHOW URL TO ADD BOT 
    @commands.Cog.listener()
    async def on_message(self, message):
        bot = self.bot
        if message.author.bot is False:
            content = message.content
            channel = message.channel
            name = bot.user.name
            content = content.upper()
            if content == f"ADD {str(name)}":
                await channel.send(url_bot)
                await bot.process_commands(message)
            if content == f"SHOW {str(name)}":
                await channel.send(file=discord.File("../src/music_under_construction.png"))
                await bot.process_commands(message)
#---------------------------_ROLE_INFO_----------------------------
    @commands.command(aliases=["r", 'role'], 
                    help='Seznam rolí.')
    async def info_role(self, ctx, role: discord.Role = None):
        if role is None:
            guild = ctx.guild
            roles = guild.roles

            embed = discord.Embed(
                    title='Seznam Rolí',
                    color = discord.Colour.greyple()
                )

            user_roles = []
            text = ""
            j = 0
            for i in range(len(roles)):
                if roles[i].is_bot_managed() == True:
                    pass
                else:
                    user_roles.append(roles[i])
                    text += f"{user_roles[j].name}\n"
                    j+=1
            text.strip()

            embed.add_field(name=f'Počet: {len(user_roles)}', value=text, inline=True)

        else:
            name = role.name
            color = role.color
            members = role.members
            members_count = len(members)
            user= ''
            for i in range(members_count):
                user += members[i].name
                if i < members_count:
                    user += '\n'
            
            embed = discord.Embed(
                    title = name,
                    color = color
                )
            embed.add_field(name=f'Uživatelé ({members_count})', value=user, inline=True)
        await ctx.send(embed=embed)
#---------------------------_USER_INFO_----------------------------
    @commands.command(aliases=['u','user'], 
                    help='Info o Uživateli.')
    async def info_user(self,ctx, username: discord.Member = None):
        if username is None:
            username = ctx.author

        nick = username.display_name

        #userID = username.id
        role = len(username.roles)-1
        topRole = username.top_role
        created = username.created_at.__format__('%d.%m. %Y')
        joined = username.joined_at.__format__('%H:%M\n%d.%m. %Y')
        avatar_url = username.avatar_url
        #status = username.status
        color: discord.Role = topRole

        author = ctx.author.display_name

        embed = discord.Embed(
                title=nick,
                description=username.mention,
                timestamp=datetime.datetime.utcnow(),
                color = color.colour
            )

        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name='Založen', value=created, inline=True)
        embed.add_field(name='Připojil se', value=joined, inline=True)
        #embed.add_field(name=f'Status', value=status, inline=True) #STATUS offline
        embed.add_field(name=f'Role ({role})', value=topRole.mention, inline=False)
        embed.set_footer(text=f"Zavolal: {author}")

        await ctx.send(embed=embed)
#--------------------------_SERVER_INFO_---------------------------
    @commands.command(aliases=['s','server'], 
                    help='Info o SERVERu.')
    async def info_server(self, ctx):
        author = ctx.author.display_name
        guild = ctx.guild

        name = guild.name
        g_id = guild.id
        icon_url = guild.icon_url
        owner = guild.owner.mention
        created = guild.created_at.__format__('%d.%m. %Y')

        member_count = guild.member_count
        members = guild.members
        bots_count = 0
        for i in members:
            if i.bot:
                bots_count += 1
        users_count = member_count-bots_count

        roles = guild.roles
        role_count = len(roles)
        
        TChannels = len(guild.text_channels)
        VChannels = len(guild.voice_channels)

        f = open(f"./guilds/{guild.id}.json", "r")
        data = json.load(f)
        try:
            url = data["URL"]
            if url == "":
                url = None
        except KeyError:
            url = None
            
        embed = discord.Embed(
            title=name,
            url=url,
            timestamp=datetime.datetime.utcnow(),
            color = discord.Colour.red()
        )

        embed.set_thumbnail(url=icon_url)
        embed.add_field(name='Zakladatel', value=owner, inline=True)
        embed.add_field(name='Server vytvořen', value=created, inline=True)
        embed.add_field(
            name=f'Místností: {TChannels+VChannels}', 
            value=f'Text.: {TChannels}\nHlas.: {VChannels}', 
            inline=True
            )

        if role_count < 3:
            role=''
            for i in range(role_count):
                role += roles[i].name
                if i < role_count:
                    role += '\n'

            embed.add_field(name=f'Rolí: {role_count}', value=role, inline=True)
        else:
            embed.add_field(name=f'Rolí:', value=role_count, inline=True)

        embed.add_field(name=f"Členů: {member_count}", value=f"Uživatelů: {users_count}\nBotů: {bots_count}", inline=True)
        embed.set_footer(text=f"\nZavolal: {author}")

        try:
            autorole = data["Autorole"]
            if autorole == "":
                autorole = None
            else:
                autorole = discord.utils.get(guild.roles, id=autorole)
                autorole = autorole.mention
                embed.add_field(name='Automatícká role:', value=autorole, inline=False)
        except KeyError:
            autorole=None
        try:
            botlog = data["BotLog"]
            if botlog == "":
                botlog = None
            else:
                botlog = discord.utils.get(guild.channels, id=botlog)
                botlog=botlog.mention
                embed.add_field(name='BotLog Channel', value=botlog, inline=False)
        except KeyError:
            botlog = None
        f.close()

        await ctx.send(embed=embed)
#----------------------------_CHANNEL_INFO_----------------------------
    @commands.command(aliases=['ch',"channel"],
                     help='Info o Channelu.')
    async def info_channel(self, ctx):
        author = ctx.author.display_name
        channel = ctx.channel
        name = channel.name

        created = channel.created_at.__format__('%d.%m. %Y')
        topic = channel.topic

        members = channel.members
        members_count = len(members)
        text = ''
        for i in range(5):
            text += members[i].name
            if i < 5:
                text += '\n'
        text += f"+{members_count-5}"
        
        embed = discord.Embed(
            title = f"Channel: __{name}__",
            color=randint(0, 0xffffff)
        )
        embed.add_field(name="Vznikl", value=created, inline=True)
        embed.add_field(name="Topic", value=topic, inline=True)
        embed.add_field(name=f"Počet uživatelů s přístupem ({members_count})", value=text, inline=False)

        await ctx.send(embed=embed)
#------------------------------------------------------------------      
def setup(bot):
    bot.add_cog(Info(bot))