# cogs/events/member_events.py

import discord
from discord.ext import commands
import logging
from datetime import datetime

class MemberEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logging.info("MemberEvents Cog initialized.")

    # Event: Member joins the guild
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logging.info(f'New member joined: {member.name}#{member.discriminator} (ID: {member.id})')
        
        # Fetch configurations
        welcome_channel_id = int(self.bot.config['welcome_channel_id'])
        default_role_name = self.bot.config['default_role_name']

        # Define the channel where welcome messages will be sent
        channel = member.guild.get_channel(welcome_channel_id)
        
        if channel is not None:
            # Create an embed for a richer welcome message
            embed = discord.Embed(
                title="Welcome!",
                description=f"Hello {member.mention}, welcome to **{member.guild.name}**! We're glad to have you here. 🎉",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")
            
            try:
                await channel.send(embed=embed)
                logging.info(f'Sent welcome message to {member.name}')
            except discord.Forbidden:
                logging.error(f"Permission denied: Cannot send messages in the welcome channel (ID: {welcome_channel_id}).")
            except Exception as e:
                logging.error(f"Failed to send welcome message: {e}")
        else:
            logging.error(f"Welcome channel with ID {welcome_channel_id} not found. Please verify the channel ID.")
        
        # Assign a default role to the new member
        default_role = discord.utils.get(member.guild.roles, name=default_role_name)
        
        if default_role is not None:
            try:
                await member.add_roles(default_role)
                logging.info(f"Assigned role '{default_role_name}' to {member.name}.")
            except discord.Forbidden:
                logging.error(f"Permission denied: Cannot assign role '{default_role_name}' to {member.name}.")
            except Exception as e:
                logging.error(f"Failed to assign role '{default_role_name}' to {member.name}: {e}")
        else:
            logging.error(f"Role '{default_role_name}' not found. Please create the role or update the role name in the Cog.")

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEvents(bot))
    logging.info("MemberEvents Cog has been added to the bot.")
    