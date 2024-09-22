# main.py

import discord
import json
from discord.ext import commands
import os
import asyncio

# Load your token from token.json
with open('token.json', 'r') as f:
    YOUR_TOKEN = json.load(f)['token']

# Replace with your actual Guild ID
GUILD_ID = 934311718237134879  # Replace with your actual Guild ID

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Enable access to message content
        intents.members = True  # Enable member events
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        # Load all cogs
        await self.load_extensions()
        # Sync commands to the specified guild
        guild = discord.Object(id=GUILD_ID)
        await self.tree.sync(guild=guild)
        print(f'Synced commands to guild {GUILD_ID}')

    async def load_extensions(self):
        # Load cogs from cogs/commands and cogs/events
        for folder in ['commands', 'events']:
            cog_directory = f'cogs/{folder}'
            for filename in os.listdir(cog_directory):
                if filename.endswith('.py') and not filename.startswith('__'):
                    extension = f'cogs.{folder}.{filename[:-3]}'
                    try:
                        await self.load_extension(extension)
                        print(f'Loaded extension: {extension}')
                    except Exception as e:
                        print(f'Failed to load extension {extension}: {e}')

# Initialize the bot
client = Client()

# Run the bot
async def main():
    async with client:
        await client.start(YOUR_TOKEN)

# Execute the bot
asyncio.run(main())
