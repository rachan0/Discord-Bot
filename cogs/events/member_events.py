# cogs/events/member_events.py

import discord
from discord.ext import commands

# Replace with your actual Guild ID
GUILD_ID = 934311718237134879  # Replace with your actual Guild ID

class MemberEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("MemberEvents Cog initialized.")

    # Event: Member joins the guild
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f'New member joined: {member.name}#{member.discriminator} (ID: {member.id})')
        
        # Define the channel where welcome messages will be sent
        welcome_channel_id = 1287398700867649577  # Replace with your welcome channel ID
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
                print(f'Sent welcome message to {member.name}')
            except discord.Forbidden:
                print(f"Permission denied: Cannot send messages in the welcome channel (ID: {welcome_channel_id}).")
            except Exception as e:
                print(f"Failed to send welcome message: {e}")
        else:
            print(f"Welcome channel with ID {welcome_channel_id} not found. Please verify the channel ID.")

        # Assign a default role to the new member
        default_role_name = "Member"  # Replace with your default role name
        default_role = discord.utils.get(member.guild.roles, name=default_role_name)
        
        if default_role is not None:
            try:
                await member.add_roles(default_role)
                print(f"Assigned role '{default_role_name}' to {member.name}.")
            except discord.Forbidden:
                print(f"Permission denied: Cannot assign role '{default_role_name}' to {member.name}.")
            except Exception as e:
                print(f"Failed to assign role '{default_role_name}' to {member.name}: {e}")
        else:
            print(f"Role '{default_role_name}' not found. Please create the role or update the role name in the Cog.")

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEvents(bot))
    print("MemberEvents Cog has been added to the bot.")
