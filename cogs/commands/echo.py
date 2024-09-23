# cogs/commands/echo.py

import discord
from discord import app_commands
from discord.ext import commands
import logging
# import os

# GUILD_ID = int(os.getenv('GUILD_ID')) #Temporary Solution for now...
class Echo(commands.Cog):
    """A Cog for echoing user messages."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="echo",
        description="Echoes your message."
    )
    @app_commands.describe(message="The message to echo back.")
    async def echo(self, interaction: discord.Interaction, message: str):
        """
        Echoes the provided message back to the user.

        Parameters:
            interaction (discord.Interaction): The interaction context.
            message (str): The message to echo.
        """
        await interaction.response.send_message(message)
        logging.info(f'Echoed message for user {interaction.user.id}: {message}')

async def setup(bot: commands.Bot):
    await bot.add_cog(Echo(bot))
    logging.info("Echo Cog has been added to the bot.")
