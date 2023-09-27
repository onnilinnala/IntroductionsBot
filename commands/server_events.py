import datetime

import hikari
import lightbulb

plugin = lightbulb.Plugin('ServerEvents')


# Events


# Join event
@plugin.listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    guild = event.get_guild()
    role_default = (await event.member.fetch_roles())[0]
    channel = await guild.create_text_channel(name=f"{event.member.username}",
                                              category=[INTRO CATEGORY ID],
                                              permission_overwrites=[
                                                  hikari.PermissionOverwrite(
                                                      id=event.member.id,
                                                      type=hikari.PermissionOverwriteType.MEMBER,
                                                      allow=(hikari.Permissions.VIEW_CHANNEL)
                                                  ),
                                                  hikari.PermissionOverwrite(
                                                      id=role_default.id,
                                                      type=hikari.PermissionOverwriteType.ROLE,
                                                      deny=(hikari.Permissions.VIEW_CHANNEL)
                                                  )
                                              ])
    # Write instruction text
    await channel.send(f"*Enter instructions*")


# Message event
@plugin.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent) -> None:
    guild = event.get_guild()
    channel_id = event.channel_id
    username = event.author.username
    if event.is_human:
        if guild.get_channel(channel=channel_id).parent_id == [INTRO CATEGORY ID]:
            if event.author.id in list(guild.get_channel(channel=channel_id).permission_overwrites):
                messages = (
                    await plugin.app.rest.fetch_messages(channel_id).take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at)
                )
                if len(messages) <= 2:
                    embed = hikari.Embed(title=f"New introduction from {username}", description=f"https://discord.com/channels/{guild.id}/{channel_id}/{event.message.id}")
                    await guild.get_channel(channel=[VERIFIER CHAT ID]).send(embed)



def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
