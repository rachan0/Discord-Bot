# cogs/commands/add_game.py

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import logging

class AddGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @app_commands.command(
        name="addgame",
        description="Add a game record."
    )
    @app_commands.describe(game_type="Type of the game.", result="Result of the game.")
    async def add_game(self, interaction: discord.Interaction, game_type: str, result: str):
        user_id = interaction.user.id
        timestamp = datetime.utcnow().isoformat()
        

async def setup(bot: commands.Bot):
    await bot.add_cog(AddGame(bot))
    logging.info("AddGame Cog has been added to the bot.")
