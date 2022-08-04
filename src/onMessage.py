from dbUtil import *
from api import *

def messageResponse(discord, client, content, author):

    content = content.replace('<@' + str(client.user.id) + '>', 'jedi')

    if author.nick == None:
        user = author.name
    else:
        user = author.nick

    if 'jedi' in content.lower():
        if 'hello' in content.lower() or 'hi' in content.lower() or 'hey' in content.lower() or 'yo' in content.lower():
            return 'Hi ' + str(user) + '!';

    if content.lower().strip() == 'jedi':
        return 'What do you want? Try `jedi help` maybe.'

    if content.lower().strip() == 'jedi help' or content.lower().strip() == 'jedihelp':
        embed = discord.Embed(title='JediBot Help', description='Oh my! You are in need of assistance? Try using one '
                                                                'of my numerous commands\n\nUsage: `jedi '
                                                                '<command>` or `@JediBot <command>`',
                              color=discord.Color.gold())
        embed.add_field(name='Commands:', value='`help`\n`stats`\n\n`kanye`\n`checkme`')
        return embed

    if content.lower().strip() == 'jedi stats' or content.lower().strip() == 'jedistats':
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

    if content.lower().strip() == 'jedi checkme':
        response = backgroundCheck(author.id)
        if not response['blacklisted']:
            return 'You have been reported ' + str(response['reports']) + ' times. You\'re also not blacklisted'
        else:
            return 'YOU ARE BLACKLISTED. YOU SHOULD BE BANNED. Reason: ' + str(response['blacklist_reason'])

    return None