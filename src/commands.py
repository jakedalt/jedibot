import sys
import traceback

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
    bot.description = "Oh my! You are in need of assistance? Try using one of my numerous commands."

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

    @bot.command(aliases=['yt'], rest_is_raw=True)
    async def youtube(ctx, search_term, *other_search_terms):
        """Searches YouTube so you don't have to (Surround term in quotes to search multiple words)

        :param search_term: (required) search term
        :param other_search_terms: (optional) more terms to include in search
        :param ctx: calling context
        """
        response = await geturl(' '.join((search_term, *other_search_terms)))
        await ctx.send(response)

    @bot.command()
    async def poll(ctx, title, option1, option2, *other_options):
        """Create a poll to gauge opinion

        :param ctx: calling context
        :param title: title of poll
        :param option1: first option for users to pick from
        :param option2: second option for users to pick from
        :param other_options: remaining options for users to pick from
        """
        # TODO could integrate further by using on_reaction_add and on_reaction_remove events
        if len(other_options) > 18:
            await ctx.send("This feature only supports up to 20 options.")
            return

        embed = discord.Embed(
            title=f"Poll: {title}",
            type='rich',
            color=discord.Color.blue()
        )
        embed.add_field(name='*Choose between the following options:*', value='\u200b')
        unicode_emojis = [u'\U0001F1E6', u'\U0001F1E7', u'\U0001F1E8', u'\U0001F1E9', u'\U0001F1EA', u'\U0001F1EB',
                          u'\U0001F1EC', u'\U0001F1ED', u'\U0001F1EE', u'\U0001F1EF', u'\U0001F1F0', u'\U0001F1F1',
                          u'\U0001F1F2', u'\U0001F1F3', u'\U0001F1F4', u'\U0001F1F5', u'\U0001F1F6', u'\U0001F1F7',
                          u'\U0001F1F8']

        max_idx = 0
        for idx, opt in enumerate((option1, option2, *other_options)):
            embed.add_field(
                name=f'{unicode_emojis[idx]}\t{opt}',
                value='\u200b',
                inline=False
            )
            max_idx += 1
        embed.set_footer(text="Vote by clicking on one of the reactions below.")
        message = await ctx.send(embed=embed)
        for i in range(max_idx):
            await message.add_reaction(unicode_emojis[i])

    async def on_command_error(ctx, error):
        # TODO see https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#exceptions for more exceptions
        if isinstance(error, commands.MissingRequiredArgument):
            message = f"Usage: `{ctx.bot.command_prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
        else:
            # print traceback for logging purposes
            print(f"Handled exception in command '{ctx.command}':", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            message = f'Error: {error}'
        await ctx.send(message)

    bot.on_command_error = on_command_error
