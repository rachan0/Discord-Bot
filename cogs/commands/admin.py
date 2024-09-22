# cogs/commands/admin.py

import discord
from discord.ext import commands
import logging

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_cog(self, ctx, extension: str):
        """Reloads a specified Cog."""
        try:
            await self.bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'Reloaded `{extension}` successfully.')
            logging.info(f'Reloaded Cog: {extension}')
        except Exception as e:
            await ctx.send(f'Failed to reload `{extension}`.')
            logging.error(f'Error reloading Cog {extension}: {e}')

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
