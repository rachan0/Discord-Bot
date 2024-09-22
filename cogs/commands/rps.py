# cogs/commands/rps.py

import discord
from discord import app_commands
from discord.ext import commands
import random

# Replace with your actual Guild ID
GUILD_ID = 934311718237134879  # Replace with your actual Guild ID

class RPS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.choices = ["rock", "paper", "scissors"]

    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="rps",
        description="Let's Play Rock Paper Scissors"
    )
    @app_commands.describe(choice="Choose rock, paper, or scissors")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors")
    ])
    async def play_rps(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        user_choice = choice.value.lower()
        bot_choice = random.choice(self.choices)

        # Determine the outcome
        if user_choice == bot_choice:
            result = "It's a tie! 🤝"
        elif (
            (user_choice == "rock" and bot_choice == "scissors") or
            (user_choice == "paper" and bot_choice == "rock") or
            (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "You win! 🎉"
        else:
            result = "You lose! 😢"

        # Create an embed for better presentation
        embed = discord.Embed(
            title="Rock Paper Scissors",
            color=discord.Color.blue()
        )
        embed.add_field(name="Your Choice", value=user_choice.capitalize(), inline=True)
        embed.add_field(name="Bot's Choice", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        embed.set_footer(text=f"Played by {interaction.user}", icon_url=interaction.user.display_avatar.url if interaction.user.display_avatar else None)

        await interaction.response.send_message(embed=embed)

    @play_rps.error
    async def play_rps_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            await interaction.response.send_message("An error occurred while processing your command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An unexpected error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RPS(bot))
