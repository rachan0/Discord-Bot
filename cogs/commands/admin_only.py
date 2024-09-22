# cogs/commands/admin_only.py

import discord
from discord.ext import commands
import logging

class AdminOnly(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='shutdown')
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """Shuts down the bot. Administrator only."""
        await ctx.send("Shutting down...")
        await self.bot.close()
        logging.info("Bot shutdown initiated by administrator.")

    @shutdown.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 You don't have permission to use this command.")
        else:
            await ctx.send("❗ An unexpected error occurred.")
            logging.error(f'Error in shutdown command: {error}')

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminOnly(bot))
    logging.info("AdminOnly Cog has been added to the bot.")
