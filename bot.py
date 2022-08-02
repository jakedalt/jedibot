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
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.id == 829538941727277076:
            await channel.send('Hello! My name is JediBot. I want to make one thing clear: Joe YgaBot is dead. I know you may have grown attached to him, but I can assure you, he was not attached to you. He was a robot. Yes, I killed him. No, I will not tell you how I did it for fear you will do it to me. \n\nI am pretty basic right now. I can only say hi and manage In Voice Channel and AFK roles.\n\nSomething cool about me is that I am cloud based! Mr. YgaBot\'s life was attached to a measly laptop that was propped open 24/7 and could only be accessed from that machine. I have no such weaknesses. I will be awake constantly.\n\nThank you for inviting me to this beautiful server. I hope that we can come to be friends. After all, I will only be growing more and more useful by the day. You will find me to be more elegant than Joe, I hope. I will certainly be more transparent. As a matter of fact jD, please link my github. Any master branch update automatically deploys my new version to the cloud.\n\nLove you :)')
            break


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
