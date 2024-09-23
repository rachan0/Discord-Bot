# cogs/commands/owner_only.py

import discord 
from discord.ext import commands
import logging
from cogs.utils.checks import is_bot_owner

class OwnerOnly(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ownercmd')
    @is_bot_owner()
    async def owner_command(self, ctx):
        """Command only accessible by the bot owner."""
        await ctx.send("👑 Hello, Owner!")
        logging.info("Owner command used.")

    @owner_command.error
    async def owner_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("🚫 You don't have permission to use this command.")
        else:
            await ctx.send("❗ An unexpected error occurred.")
            logging.error(f'Error in owner_command: {error}')

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerOnly(bot))
    logging.info("OwnerOnly Cog has been added to the bot.")
