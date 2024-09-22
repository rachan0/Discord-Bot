# cogs/events/general_events.py

import discord
from discord.ext import commands
import logging

class GeneralEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logging.info("GeneralEvents Cog initialized.")

    # Event: Bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Bot is ready. Logged in as {self.bot.user}!')

    # Event: Message received
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('Hello'):
            await message.channel.send(f'Hi there! {message.author.mention}')
            logging.info(f"Responded to 'Hello' from {message.author}")

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralEvents(bot))
    logging.info("GeneralEvents Cog has been added to the bot.")
