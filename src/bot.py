import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from on_message import message_response
from db_util import message_received, vc_join
from api import background_check


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for jedi help"))
    daily_job.start()


@tasks.loop(hours=24)
async def daily_job():
    print('Daily job commenced')


@client.event
async def on_member_join(member):
    report = background_check(member.id)
    if not report['blacklisted']:
        if report['reports'] == 0:
            await member.create_dm()
            await member.dm_channel.send(
                f'Hello there, {member.name}! True Jedi welcomes you.'
            )
            channel = member.guild.text_channels[0]
            if channel is not None:
                channel.send('Everyone welcome ' +
                             member.name + ' to True Jedi! They passed my background check with flying colors.')
        else:
            await member.create_dm()
            await member.dm_channel.send(
                f'Hello there, {member.name}! True Jedi welcomes you. You do have some reports, but if you are well-'
                f'behaved, we will love having you on True Jedi'
            )
            channel = member.guild.text_channels[0]
            if channel is not None:
                channel.send(member.name + ' has joined True Jedi. My background check dug up ' +
                             str(report['reports']) +
                             ' reports. There is a good chance that these reports were not substantial.')
    else:
        channel = member.guild.text_channels[0]
        if channel is not None:
            channel.send('***WARNING!***')
            channel.send('WARNING! ' + member.name + ' is known to be a dangerous and blacklisted Discord user with ' +
                         str(report['reports']) + '. Blacklist reason: ' + str(report['blacklist_reason']))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    else:
        await message_received(message.author.id)
        response = await message_response(discord, client, message)
        if response is not None:
            if type(response) == discord.Embed:
                await message.channel.send(embed=response)
            else:
                await message.channel.send(response)


@client.event
async def on_voice_state_update(member, before, after):
    ivc = False
    afk = False

    if after.channel is None:
        preposition = before
    else:
        preposition = after

    for role in preposition.channel.guild.roles:
        if role.name == 'In Voice Channel':
            ivc = True
            afk = True
    if not ivc:
        await preposition.channel.guild.create_role(
            name='In Voice Channel',
            permissions=discord.Permissions.none(),
            colour=discord.Colour(0x2ecc71),
            hoist=True,
            mentionable=True,
            reason='IVC needed'
        )
    if not afk:
        await preposition.channel.guild.create_role(
            name='AFK',
            permissions=discord.Permissions.none(),
            colour=discord.Colour(0xbf0000),
            hoist=True,
            mentionable=True,
            reason='AFK needed'
        )

    if after.channel is None:
        for role in before.channel.guild.roles:
            if role.name == 'In Voice Channel':
                await member.remove_roles(role, reason='Left voice')
        for role in before.channel.guild.roles:
            if role.name == 'AFK':
                await member.remove_roles(role, reason='Left AFk')

    elif after.channel.id == 672976147218300951:
        if not member.bot:
            await vc_join(member.id)
        for role in after.channel.guild.roles:
            if role.name == 'In Voice Channel':
                await member.remove_roles(role, reason='Left voice')

            afk_role = None
            for role1 in after.channel.guild.roles:
                if role1.name == 'AFK':
                    afk_role = role1
        await member.add_roles(afk_role, reason='Joined AFK')

    else:
        if not member.bot:
            await vc_join(member.id)
        for role in after.channel.guild.roles:
            if role.name == 'AFK':
                await member.remove_roles(role, reason='Left AFk')

            ivc_role = None
            for role1 in after.channel.guild.roles:
                if role1.name == 'In Voice Channel':
                    ivc_role = role1
        await member.add_roles(ivc_role, reason='Joined voice')

client.run(TOKEN)
