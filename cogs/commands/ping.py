# cogs/commands/ping.py

import discord
from discord import app_commands
from discord.ext import commands

# Replace with your actual Guild ID
# import os

# GUILD_ID = int(os.getenv('GUILD_ID'))

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="ping",
        description="Check the bot's latency."
    )
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await interaction.response.send_message(f'Pong! Latency: {latency:.2f}ms')

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
