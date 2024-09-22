# main.py

import discord
import os
import asyncio
import logging
from discord.ext import commands
from dotenv import load_dotenv
import logger  # Ensure logger.py is properly set up

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger.setup_logging()

# Extract configuration variables
YOUR_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')
DEFAULT_ROLE_NAME = os.getenv('DEFAULT_ROLE_NAME')

# Validate essential configurations
if not all([YOUR_TOKEN, GUILD_ID, WELCOME_CHANNEL_ID, DEFAULT_ROLE_NAME]):
    logging.error("Missing one or more required environment variables.")
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
        intents.voice_states = True  # Enable voice state events
        super().__init__(command_prefix="/", intents=intents)
        self.config = {
            "guild_id": GUILD_ID,
            "welcome_channel_id": WELCOME_CHANNEL_ID,
            "default_role_name": DEFAULT_ROLE_NAME
        }  # Make config accessible to Cogs

    async def setup_hook(self):
        # Load all cogs
        await self.load_extensions()
        # Sync commands to the specified guild
        guild = discord.Object(id=self.config['guild_id'])
        try:
            synced = await self.tree.sync(guild=guild)
            logging.info(f'Synced {len(synced)} commands to guild {self.config["guild_id"]}')
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
