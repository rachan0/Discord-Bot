# cogs/commands/rate_limited.py

import discord
from discord.ext import commands
import logging

class RateLimited(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='limited')
    @commands.cooldown(rate=5, per=60, type=commands.BucketType.user)
    async def limited_command(self, ctx):
        await ctx.send("This is a rate-limited command.")
        logging.info(f"Rate-limited command used by {ctx.author.id}.")

    @limited_command.error
    async def limited_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Please try again after {round(error.retry_after, 2)} seconds.")
        else:
            await ctx.send("❗ An unexpected error occurred.")
            logging.error(f'Error in limited_command: {error}')

async def setup(bot: commands.Bot):
    await bot.add_cog(RateLimited(bot))
    logging.info("RateLimited Cog has been added to the bot.")
