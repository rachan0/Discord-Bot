# cogs/commands/hello.py

import discord
from discord import app_commands
from discord.ext import commands
import logging

class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logging.info("Hello Cog initialized.")

    @commands.Cog.listener()
    async def on_ready(self):
        # Register the /hello command
        guild = discord.Object(id=int(self.bot.config['guild_id']))
        try:
            await self.bot.tree.sync(guild=guild)
            logging.info(f"/hello command synced to guild {self.bot.config['guild_id']}")
        except Exception as e:
            logging.error(f"Failed to sync /hello command: {e}")

    @app_commands.command(
        name="hello",
        description="Say Hello!"
    )
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")
        logging.info(f"/hello command used by {interaction.user}")

    @say_hello.error
    async def say_hello_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            await interaction.response.send_message("An error occurred while processing your command.", ephemeral=True)
            logging.error(f"Error in /hello command: {error}")
        else:
            await interaction.response.send_message(f"An unexpected error occurred: {error}", ephemeral=True)
            logging.error(f"Unexpected error in /hello command: {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
    logging.info("Hello Cog has been added to the bot.")
