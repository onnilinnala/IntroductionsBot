import hikari
import lightbulb

bot = lightbulb.BotApp(
    token=[TOKEN],
    intents=hikari.Intents.ALL,
    prefix='!'
)


# Check Error Handler
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CheckFailure):
        await event.context.respond("You are not a verifier!", delete_after=5)
        pass


@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command('reload', 'Reloads all commands!')
@lightbulb.implements(lightbulb.PrefixCommand)
async def reload(ctx: lightbulb.Context) -> None:
    for extension in bot.extensions:
        bot.unload_extensions(extension)
    bot.load_extensions_from('./commands')
    await ctx.respond('Reloaded commands!')


bot.load_extensions_from('./commands')
bot.run()