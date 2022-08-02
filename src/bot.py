import os

import discord
from dotenv import load_dotenv
from onMessage import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello there, {member.name}! True Jedi welcomes you.'
    )


@client.event
async def on_message(message):
    if message.author.bot:
        return

    else:
        response = messageResponse(message.content, message.author)
        if response is not None:
            await message.channel.send(response)


@client.event
async def on_voice_state_update(member, before, after):
    ivc = False
    afk = False

    if after.channel is None:
        boA = before
    else:
        boA = after

    for role in boA.channel.guild.roles:
        if role.name == 'In Voice Channel':
            ivc = True
            afk = True
    if not ivc:
        await boA.channel.guild.create_role(name='In Voice Channel', permissions=discord.Permissions.none(),
                                              colour=discord.Colour(0x2ecc71), hoist=True, mentionable=True,
                                              reason='IVC needed')
    if not afk:
        await boA.channel.guild.create_role(name='AFK', permissions=discord.Permissions.none(),
                                              colour=discord.Colour(0xbf0000), hoist=True, mentionable=True,
                                              reason='AFK needed')

    if after.channel is None:
        for role in before.channel.guild.roles:
            if role.name == 'In Voice Channel':
                await member.remove_roles(role, reason='Left voice')
        for role in before.channel.guild.roles:
            if role.name == 'AFK':
                await member.remove_roles(role, reason='Left AFk')

    elif after.channel.id == 672976147218300951:
        for role in after.channel.guild.roles:
            if role.name == 'In Voice Channel':
                await member.remove_roles(role, reason='Left voice')

            afkrole = None
            for role in after.channel.guild.roles:
                if role.name == 'AFK':
                    afkrole = role
        await member.add_roles(afkrole, reason='Joined AFK')

    else:
        for role in after.channel.guild.roles:
            if role.name == 'AFK':
                await member.remove_roles(role, reason='Left AFk')

            ivcrole = None
            for role in after.channel.guild.roles:
                if role.name == 'In Voice Channel':
                    ivcrole = role
        await member.add_roles(ivcrole, reason='Joined voice')


client.run(TOKEN)
