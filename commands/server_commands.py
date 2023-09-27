import hikari
import lightbulb

plugin = lightbulb.Plugin('ServerCommands')


# Checks
@lightbulb.Check
async def is_intro_verifier(context: lightbulb.Context) -> bool:
    if [VERIFIER ROLE ID] in [i.id for i in await context.member.fetch_roles()]:
        return True
    return False


# Commands
@plugin.command
@lightbulb.command('ping', 'Says pong!')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.PrefixCommand) -> None:
    await ctx.respond('Pong!')


@plugin.command
@lightbulb.option("user", "The user to verify.", type=hikari.User, default=0)
@lightbulb.add_checks(is_intro_verifier)
@lightbulb.command('verify', 'Verifies user.', pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def verify(guild: lightbulb.PrefixCommand, user: hikari.User) -> None:
    if not guild.guild_id:
        await guild.respond("This command can only be used in a server.", delete_after=5)
        return
    if user == 0:
        await guild.respond("No user selected!", delete_after=5)
        return
    await guild.get_guild().get_member(user=user.id).add_role([INTRODUCED ROLE ID])
    for channel in guild.get_guild().get_channels():
        if user.id in guild.get_guild().get_channel(channel=channel).permission_overwrites:
            channel_id = int(channel)
    messages = plugin.app.rest.fetch_messages(channel_id)
    thread = await plugin.app.rest.create_thread([INTRODUCTIONS CHANNEL ID], 11, user.global_name)
    async for message in messages.reversed():
        if not message.author.is_bot:
            await plugin.app.rest.execute_webhook(webhook=[WEBHOOK ID],
                                                  token=[WEBHOOK TOKEN],
                                                  content=message.content,
                                                  username=message.author.global_name,
                                                  avatar_url=message.author.avatar_url,
                                                  thread=thread.id)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
