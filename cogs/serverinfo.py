import discord
from discord.ext import commands


class Server:
    """Server commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def server(self, ctx):
        """Server commands."""

        await self.bot.send_cmd_help(ctx)

    @server.command()
    async def info(self, ctx):
        """Various info about the guild."""

        guild = ctx.message.guild

        online = 0
        for i in guild.members:
            if str(
                    i.status) == 'online' or str(
                    i.status) == 'idle' or str(
                    i.status) == 'dnd':
                online += 1

        channels = guild.channels
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        categories = guild.categories

        role_count = len(guild.roles)
        emoji_count = len(guild.emojis)

        em = discord.Embed(title=None,
                           description=None,
                           url=None,
                           timestamp=ctx.message.created_at,
                           color=discord.Color.red())
        em.add_field(name='Name', value=guild.name)
        em.add_field(name='Owner', value=guild.owner, inline=False)
        em.add_field(name='Region', value=guild.region, inline=False)
        em.add_field(name='Highest role',
                     value=guild.role_hierarchy[0], inline=False)
        em.add_field(name='Members', value=guild.member_count)
        em.add_field(name='Currently Online', value=online)
        em.add_field(name='Text Channels', value=str(len(text_channels)))
        em.add_field(name='Voice Channels', value=str(len(voice_channels)))
        em.add_field(name='Categories', value=str(len(categories)))
        em.add_field(name='All Channels', value=str(len(channels)))
        em.add_field(
            name='Verification Level', value=str(
                guild.verification_level))
        em.add_field(
            name='Explicit Content Filter', value=str(
                guild.explicit_content_filter))

        em.add_field(name='Number of roles', value=str(role_count))
        em.add_field(name='Number of emotes', value=str(emoji_count))
        em.add_field(name='Created At', value=guild.created_at.__format__(
            '%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        em.set_thumbnail(url=guild.icon_url)
        em.set_author(name='Server Info',
                      icon_url=guild.icon_url)
        em.set_footer(text=f'Server ID: {guild.id}')

        await ctx.send(embed=em)

    @server.command()
    async def emojis(self, ctx):
        """List all emojis in this guild."""

        guild = ctx.message.guild
        emojis = (str(x) for x in guild.emojis)
        await ctx.send("".join(emojis))

    @server.command()
    async def avi(self, ctx):
        """Retrieves the guild avatar image link."""

        guild = ctx.message.guild
        em = discord.Embed(title=None,
                           description=None,
                           url=None,
                           timestamp=ctx.message.created_at,
                           color=discord.Color.red())
        em.set_image(url=guild.icon_url)
        await ctx.send(embed=em)


def setup(bot):
    cog = Server(bot)
    bot.add_cog(cog)
