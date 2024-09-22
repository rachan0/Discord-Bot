# cogs/events/general_events.py

import discord
from discord.ext import commands

class GeneralEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Event: Bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.bot.user}!')

    # Event: Message received
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('Hello'):
            await message.channel.send(f'Hi there! {message.author.mention}')

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralEvents(bot))
