# cogs/commands/hello.py

import discord
from discord import app_commands
from discord.ext import commands

# Replace with your actual Guild ID
GUILD_ID = 934311718237134879  # Replace with your actual Guild ID

class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="hello",
        description="Say Hello!"
    )
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
