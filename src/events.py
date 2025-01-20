import discord

from discord.ext import tasks
from api import background_check
from db_util import message_received, vc_join, joeLock
from constants import GREETINGS

JOEY_BINGO_PARTICIPANTS = [263361715712950272, 377627433739878400, 263345572155490304, 205416635207647233, 391374975438684170]


@tasks.loop(hours=24)
async def daily_job():
    print('Daily job commenced')


def register_events(bot):
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for jedi help"))
        print('Connected to the following server(s):')
        for guild in bot.guilds:
            print(f"\t{guild.name} (id '{guild.id}')")

        jl = await joeLock()
        print('JoeLock Rule: ' + str(jl))
        print("Ready for action!\n")
        daily_job.start()

    @bot.event
    async def on_guild_join(guild):
        if guild.id == 425799350573334528 or guild.id == 1003874309640564847:
            print('added to familiar guild')
            await guild.text_channels[0].send('I\'m back. What did I miss?')
        else:
            await guild.text_channels[0].send('I\'m sorry,'
                                              ' I\'m not meant to be here. I belong on the True Jedi server only.')
            print('added to unfamiliar guild ' + str(guild) + ': owner:' + str(guild.owner) + '\n' + str(guild.members))
            await guild.leave()

    # @bot.event
    # async def on_member_join(member):
    #     report = background_check(member.id)
    #     if not report['blacklisted']:
    #         if report['reports'] == 0:
    #             await member.create_dm()
    #             await member.dm_channel.send(
    #                 f'Hello there, {member.name}! True Jedi welcomes you.'
    #             )
    #             channel = member.guild.text_channels[0]
    #             if channel is not None:
    #                 channel.send('Everyone welcome ' +
    #                              member.name + ' to True Jedi! They passed my background check with flying colors.')
    #         else:
    #             await member.create_dm()
    #             await member.dm_channel.send(
    #                 f'Hello there, {member.name}! True Jedi welcomes you. You do have some reports, but if you are well-'
    #                 f'behaved, we will love having you on True Jedi'
    #             )
    #             channel = member.guild.text_channels[0]
    #             if channel is not None:
    #                 channel.send(member.name + ' has joined True Jedi. My background check dug up ' +
    #                              str(report['reports']) +
    #                              ' reports. There is a good chance that these reports were not substantial.')
    #     else:
    #         channel = member.guild.text_channels[0]
    #         if channel is not None:
    #             channel.send('***WARNING!***')
    #             channel.send('WARNING! ' + member.name + 'is known to be a dangerous and blacklisted Discord user with '
    #                          + str(report['reports']) + '. Blacklist reason: ' + str(report['blacklist_reason']))

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if message.author.bot:
            return  # ignore bot messages

        await message_received(message.author.id, message.author.name)
        content = message.content.replace('<@' + str(bot.user.id) + '>', 'jedi').lower()

        if 'jedi' in content and any(greeting in content for greeting in GREETINGS):
            user = message.author.nick if message.author.nick is not None else message.author.name
            await message.channel.send('Hi ' + str(user) + '!')

        # on_message also catches commands; need to pass them on for them to be processed
        await bot.process_commands(message)

    @bot.event
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
                if role.name == 'AFK':
                    await member.remove_roles(role, reason='Left AFk')

        elif after.channel.id == 672976147218300951:
            if not member.bot:
                await vc_join(member.id, member.name)
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
                await vc_join(member.id, member.name)
            if member.id == 377627433739878400:
                print('Joey Bingo Starting')
                for member_in_channel in after.channel.members:
                    if member_in_channel in JOEY_BINGO_PARTICIPANTS:
                        await member_in_channel.send(
                            f"Hey {member_in_channel.mention}, Joey has arrived in {after.channel.name}! It's time for Joey Bingo: \n\nhttps://bingobaker.com/#678d8de28fd26009\n\nTalk to JD to opt out.")

            if member.id in JOEY_BINGO_PARTICIPANTS:
                joeyPresent = False
                for member_in_channel in after.channel.members:
                    if member_in_channel == 377627433739878400:
                        joeyPresent = True
                if joeyPresent:
                    print('Joey Bingo Player Added')
                    await member.send(
                        f"Hey {member.mention}, Joey is in {after.channel.name}! It's time for Joey Bingo: \n\nhttps://bingobaker.com/#678d8de28fd26009\n\nTalk to JD to opt out.")

            for role in after.channel.guild.roles:
                if role.name == 'AFK':
                    await member.remove_roles(role, reason='Left AFk')

                ivc_role = None
                for role1 in after.channel.guild.roles:
                    if role1.name == 'In Voice Channel':
                        ivc_role = role1
            await member.add_roles(ivc_role, reason='Joined voice')
