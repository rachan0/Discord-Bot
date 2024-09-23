# cogs/commands/hello.py

import discord
from discord import app_commands
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @app_commands.command(
        name="hello",
        description="Say Hello!"
    )
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
