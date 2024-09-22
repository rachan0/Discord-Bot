# main.py

import discord
import json
from discord.ext import commands
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

# Load configuration from token.json
CONFIG_PATH = 'token.json'

if not os.path.exists(CONFIG_PATH):
    logging.error(f"Configuration file '{CONFIG_PATH}' not found.")
    exit(1)

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
    logging.error("Missing one or more required configurations in 'token.json'.")
    exit(1)

# Convert IDs to integers
try:
    GUILD_ID = int(GUILD_ID)
    WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID)
except ValueError:
    logging.error("Guild ID and Welcome Channel ID must be integers.")
    exit(1)

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Enable access to message content
        intents.members = True  # Enable member events
        super().__init__(command_prefix="/", intents=intents)
        self.config = config  # Make config accessible to Cogs

    async def setup_hook(self):
        # Load all cogs
        await self.load_extensions()
        # Sync commands to the specified guild
        guild = discord.Object(id=GUILD_ID)
        try:
            synced = await self.tree.sync(guild=guild)
            logging.info(f'Synced {len(synced)} commands to guild {GUILD_ID}')
        except Exception as e:
            logging.error(f'Error syncing commands: {e}')

    async def load_extensions(self):
        # Load cogs from cogs/commands and cogs/events
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
                        logging.info(f'Loaded extension: {extension}')
                    except Exception as e:
                        logging.error(f'Failed to load extension {extension}: {e}')

# Initialize the bot
client = Client()

# Run the bot
async def main():
    async with client:
        await client.start(YOUR_TOKEN)

# Execute the bot
if __name__ == "__main__":
    asyncio.run(main())
