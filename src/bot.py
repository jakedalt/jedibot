from discord.ext.commands import Bot
from commands import register_commands
from events import register_events
from constants import TOKEN


bot = Bot(command_prefix='jedi ')


if __name__ == '__main__':
    register_events(bot)
    register_commands(bot)
    bot.run(TOKEN)
