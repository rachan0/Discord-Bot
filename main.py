import discord
from discord.ext import commands

import logging
from dotenv import load_dotenv
import os
GUILD_ID = int(os.getenv('GUILD_ID'))
# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)

# Configure intents
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content
intents.members = True          # Enable member events
intents.voice_states = True     # Enable voice state events

# Initialize the bot
bot = commands.Bot(command_prefix='/', intents=intents)

async def load_extensions():
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
                    await bot.load_extension(extension)
                    logging.info(f'Loaded extension: {extension}')
                except Exception as e:
                    logging.error(f'Failed to load extension {extension}: {e}')


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')
    await load_extensions()
    try:
        guild = discord.Object(id=GUILD_ID)  # Replace with your guild ID
        synced = await bot.tree.sync(guild=guild)
        logging.info(f'Synced {len(synced)} commands to guild {guild.id}.')
    except Exception as e:
        logging.error(f'Error syncing commands: {e}')


# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
