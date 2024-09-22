# cogs/commands/greet.py

import discord
from discord import app_commands
from discord.ext import commands
import logging

class Greet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="greet",
        description="Greet a user."
    )
    @app_commands.describe(user="The user to greet.")
    async def greet(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f"Hello, {user.mention}! 👋")
        logging.info(f"Greeted user {user} in guild {interaction.guild.id}.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Greet(bot))
    logging.info("Greet Cog has been added to the bot.")
