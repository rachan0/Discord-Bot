# main.py

import discord
import json
from discord.ext import commands
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),  # Logs will be saved to bot.log
        logging.StreamHandler()           # Logs will also be output to the console
    ]
)

# Path to your configuration file
CONFIG_PATH = 'token.json'

# Check if the configuration file exists
if not os.path.exists(CONFIG_PATH):
    logging.error(f"Configuration file '{CONFIG_PATH}' not found. Please ensure it exists in the project directory.")
    exit(1)

# Load configuration from token.json
with open(CONFIG_PATH, 'r') as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from '{CONFIG_PATH}': {e}")
        exit(1)

# Extract configuration variables
YOUR_TOKEN = config.get('token')
GUILD_ID = config.get('guild_id')
WELCOME_CHANNEL_ID = config.get('welcome_channel_id')
DEFAULT_ROLE_NAME = config.get('default_role_name')

# Validate essential configurations
if not all([YOUR_TOKEN, GUILD_ID, WELCOME_CHANNEL_ID, DEFAULT_ROLE_NAME]):
    logging.error("Missing one or more required configurations in 'token.json'. Please ensure 'token', 'guild_id', 'welcome_channel_id', and 'default_role_name' are set.")
    exit(1)

# Convert IDs to integers (Discord IDs are integers)
try:
    GUILD_ID = int(GUILD_ID)
    WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID)
except ValueError:
    logging.error("Guild ID and Welcome Channel ID must be integers.")
    exit(1)

class MyBot(commands.Bot):
    def __init__(self):
        # Define intents
        intents = discord.Intents.default()
        intents.message_content = True  # Required for accessing message content
        intents.members = True          # Required for member-related events like on_member_join

        # Initialize the Bot with the specified command prefix and intents
        super().__init__(command_prefix="/", intents=intents)

        # Assign the loaded configuration to the bot instance for easy access in Cogs
        self.config = config

    async def setup_hook(self):
        # Load all Cogs/extensions
        await self.load_extensions()

        # Sync commands to the specified guild (for faster command availability)
        guild = discord.Object(id=GUILD_ID)
        try:
            synced_commands = await self.tree.sync(guild=guild)
            logging.info(f"Synced {len(synced_commands)} commands to guild ID {GUILD_ID}.")
        except Exception as e:
            logging.error(f"Failed to sync commands to guild ID {GUILD_ID}: {e}")

    async def load_extensions(self):
        """
        Dynamically load all Cogs from the 'cogs/commands' and 'cogs/events' directories.
        """
        for folder in ['commands', 'events']:
            cog_directory = f'cogs/{folder}'
            if not os.path.isdir(cog_directory):
                logging.warning(f"Cog directory '{cog_directory}' does not exist. Skipping.")
                continue

            for filename in os.listdir(cog_directory):
                if filename.endswith('.py') and not filename.startswith('__'):
                    extension = f'cogs.{folder}.{filename[:-3]}'
                    try:
                        await self.load_extension(extension)
                        logging.info(f"Loaded extension: {extension}")
                    except Exception as e:
                        logging.error(f"Failed to load extension '{extension}': {e}")

# Initialize the bot
bot = MyBot()

# Run the bot
async def main():
    async with bot:
        await bot.start(YOUR_TOKEN)

# Execute the bot
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot has been manually stopped.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")
