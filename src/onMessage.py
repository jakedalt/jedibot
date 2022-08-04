from dbUtil import *
from api import *

def messageResponse(discord, content, author):

    if author.nick == None:
        user = author.name
    else:
        user = author.nick

    if 'jedibot' in content.lower():
        if 'hello' in content.lower() or 'hi' in content.lower() or 'hey' in content.lower() or 'yo' in content.lower():
            return 'Hi ' + str(user) + '!';

    if content.lower().strip() == 'jedibot':
        return 'What do you want? Try `jedi help` maybe.'

    if content.lower().strip() == 'jedi help':
        embed = discord.Embed(title='JediBot Help', description='Oh my! You are in need of assistance? Try using one of my numerous commands\n\nUsage: `jedi <command>`',color=discord.Color.gold())
        embed.add_field(name='Commands:', value='`help`\n`stats`')
        return embed

    if content.lower().strip() == 'jedi stats':
        stats = getUserStats(author.id)
        if stats is None:
            print('stat error, getUserStats returned None: ' + str(author.name) + ' id: ' + str(author.id))
            return 'Something must be wrong, because you don\'t have any stats.'
        embed = discord.Embed(title=str(user) + '\'s Stats',
                              description='*in the JediBot era*',
                              color=discord.Color.blue())
        embed.add_field(name='Text Messages Sent', value=stats[0], inline=True)
        embed.add_field(name='Voice Channel Joins', value=stats[1], inline=True)

        return embed

    if content.lower().strip() == 'jedi kanye':
        return kanye()['quote']

    return None