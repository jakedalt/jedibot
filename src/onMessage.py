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
        embed = discord.Embed(title='JediBot Help', description='Oh my! You are in need of assistance? Try using one of my numerous commands\n\nUsage: `jedi <command>`',color=discord.Color.blue())
        embed.add_field(name='Commands:', value='`help`')
        return embed

    if content.lower().strip() == 'jedi stats':
        return 'I\'ll implement this soon'

    return None