def messageResponse(content, author):

    if author.nick == None:
        user = author.name
    else:
        user = author.nick

    if 'jedibot' in content.lower():
        if ('hello' or 'hi' or 'hey' or 'yo') in content.lower():
            return 'Hi ' + str(user) + '!';

    if content.lower().strip() == 'jedibot':
        return 'What do you want? Try `jedi help` maybe.'

    if content.lower().strip() == 'jedi help':
        return 'I\'ll implement this soon'

    return None