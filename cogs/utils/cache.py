# cogs/utils/cache.py

import asyncio
import logging

class Cache:
    def __init__(self):
        self.guild_info = {}

    async def load_guild_info(self, bot):
        for guild in bot.guilds:
            self.guild_info[guild.id] = {
                "name": guild.name,
                "member_count": guild.member_count
            }
            logging.info(f"Cached info for guild: {guild.name} ({guild.id})")

cache = Cache()
