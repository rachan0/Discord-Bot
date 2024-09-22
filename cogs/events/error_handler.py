# cogs/events/error_handler.py

import discord
from discord.ext import commands
import logging

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Event listener for on_command_error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("🔍 Command not found. Please check the command and try again.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Missing arguments. Please provide all required information.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("🚫 You do not have permission to use this command.")
        else:
            await ctx.send("❗ An unexpected error occurred. Please try again later.")
            logging.error(f'Unhandled exception: {error}')

    # Event listener for on_application_command_error (for Slash Commands)
    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.CommandNotFound):
            await interaction.response.send_message("🔍 Command not found. Please check the command and try again.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message("⚠️ Missing arguments. Please provide all required information.", ephemeral=True)
        elif isinstance(error, commands.NotOwner):
            await interaction.response.send_message("🚫 You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("❗ An unexpected error occurred. Please try again later.", ephemeral=True)
            logging.error(f'Unhandled exception in Slash Command: {error}')

async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))
    logging.info("ErrorHandler Cog has been added to the bot.")
