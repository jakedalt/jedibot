import discord

from discord.ext import commands
from api import background_check, kanye
from db_util import get_user_stats
from youtube_player import geturl
from constants import ENVIRONMENT


# TODO - extend HelpCommand to be more customized
#  show aliases, have nicer embed with colors like JD's help method
class JediHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__(no_category="Uncategorized Commands")

    def get_ending_note(self):
        return 'Type `jedi help <command>` for more info on a command.\n' \
               'You can also type `jedi help <category> for more info on a category.'


def register_commands(bot):

    bot.help_command = JediHelpCommand()  # register custom help command

    @bot.command()
    async def info(ctx):
        """Describes the bot's runtime environment

        :param ctx: calling context
        """
        await ctx.send(f'I am a bot running on {ENVIRONMENT} with discordpy version {discord.__version__}.')

    @bot.command(name='help!')
    async def jedi_help(ctx):
        """Displays JD's legacy help menu

        :param ctx: calling context
        """
        embed = discord.Embed(
            title='JediBot Help',
            description='*This is the legacy help menu. Ideally, the new menu would look like this one.*\n\n'
                        'Oh my! You are in need of assistance? Try using one of my numerous commands\n\n'
                        'Usage: `jedi <command>`',
            color=discord.Color.gold()
        )
        embed.add_field(
            name='Commands:',
            value="For commands, type `jedi help`.\n\n*Isn't this beautiful?*"
        )
        await ctx.send(embed=embed)

    @bot.command(name='stats')
    async def jedi_stats(ctx):
        """Reveals your stats (in the JediBot era)

        :param ctx: calling context
        """
        stats = get_user_stats(ctx.author.id)
        if stats is None:
            print('stat error, getUserStats returned None: ' + str(ctx.author.name) + ' id: '
                  + str(ctx.author.id))
            await ctx.send('Something must be wrong, because you don\'t have any stats.')
        else:
            user = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
            embed = discord.Embed(title=str(user) + '\'s Stats',
                                  description='*in the JediBot era*',
                                  color=discord.Color.blue())
            embed.add_field(name='Text Messages Sent', value=stats[0], inline=True)
            embed.add_field(name='Voice Channel Joins', value=stats[1], inline=True)
            await ctx.send(embed=embed)

    @bot.command(aliases=['bg'])
    async def background(ctx):
        """Performs a background check on you

        :param ctx: calling context
        """
        response = background_check(ctx.author.id)
        if not response['blacklisted']:
            message = 'You have been reported ' + str(response['reports']) + ' times. You\'re also not blacklisted'
        else:
            message = 'YOU ARE BLACKLISTED. YOU SHOULD BE BANNED. Reason: ' + str(response['blacklist_reason'])
        await ctx.send(message)

    @bot.command(name='kanye')
    async def jedi_kanye(ctx):
        """Consults Kanye for inspiration

        :param ctx: calling context
        """
        await ctx.send(kanye()['quote'])

    @bot.command(aliases=['yt'])
    async def youtube(ctx, query):
        """Searches YouTube so you don't have to (Surround term in quotes to search multiple words)

        :param ctx: calling context
        :param query: phrase to search with
        """
        response = await geturl(query)
        await ctx.send(response)
