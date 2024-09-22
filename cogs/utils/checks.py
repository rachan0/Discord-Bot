# cogs/utils/checks.py

from discord.ext import commands

def is_bot_owner():
    async def predicate(ctx):
        return ctx.author.id == 620830203320467467  # Replace with your Discord User ID
    return commands.check(predicate)
