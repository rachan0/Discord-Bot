# cogs/commands/music.py

import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
import logging

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

GUILD_ID = 934311718237134879
class Music(commands.Cog):
    """Music related commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_clients = {}  # To manage multiple guilds
        self.music_queues = {}    # To manage music queues per guild

    
    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="play",
        description="Play a song from YouTube."
    )
    @app_commands.describe(song="The name or URL of the song to play.")
    async def play(self, interaction: discord.Interaction, song: str):
        """Plays a song from YouTube in the user's voice channel."""
        await interaction.response.defer()

        voice_channel = interaction.user.voice.channel if interaction.user.voice else None
        if not voice_channel:
            await interaction.followup.send("🔴 You are not connected to a voice channel.", ephemeral=True)
            return

        if interaction.guild.id not in self.voice_clients:
            voice_client = await voice_channel.connect()
            self.voice_clients[interaction.guild.id] = voice_client
            self.music_queues[interaction.guild.id] = []
        else:
            voice_client = self.voice_clients[interaction.guild.id]

        if voice_client.is_playing():
            self.music_queues[interaction.guild.id].append(song)
            await interaction.followup.send(f"🎶 Added **{song}** to the queue.", ephemeral=True)
            logging.info(f'Added {song} to queue in guild {interaction.guild.id}')
            return

        try:
            source = await YTDLSource.from_url(song, loop=self.bot.loop, stream=True)
            voice_client.play(source, after=lambda e: self.play_next(interaction.guild.id, e))
            await interaction.followup.send(f"🎶 Now playing: **{source.title}**")
            logging.info(f'Playing {source.title} in guild {interaction.guild.id}')
        except Exception as e:
            logging.error(f"Error playing song: {e}")
            await interaction.followup.send("❌ An error occurred while trying to play the song.", ephemeral=True)

    
    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="stop",
        description="Stop the music and disconnect the bot from the voice channel."
    )
    async def stop(self, interaction: discord.Interaction):
        """Stops the music and disconnects the bot from the voice channel."""
        voice_client = self.voice_clients.get(interaction.guild.id)

        if not voice_client or not voice_client.is_connected():
            await interaction.response.send_message("🔴 I am not connected to any voice channel.", ephemeral=True)
            return

        voice_client.stop()
        await voice_client.disconnect()
        del self.voice_clients[interaction.guild.id]
        del self.music_queues[interaction.guild.id]
        await interaction.response.send_message("🛑 Stopped the music and disconnected from the voice channel.")
        logging.info(f'Disconnected from voice channel in guild {interaction.guild.id}')

    
    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="pause",
        description="Pause the currently playing song."
    )
    async def pause(self, interaction: discord.Interaction):
        """Pauses the currently playing song."""
        voice_client = self.voice_clients.get(interaction.guild.id)

        if not voice_client or not voice_client.is_playing():
            await interaction.response.send_message("🔴 No song is currently playing.", ephemeral=True)
            return

        voice_client.pause()
        await interaction.response.send_message("⏸️ Paused the current song.")
        logging.info(f'Paused music in guild {interaction.guild.id}')

    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="resume",
        description="Resume the paused song."
    )
    async def resume(self, interaction: discord.Interaction):
        """Resumes a paused song."""
        voice_client = self.voice_clients.get(interaction.guild.id)

        if not voice_client or not voice_client.is_paused():
            await interaction.response.send_message("🔴 No song is paused currently.", ephemeral=True)
            return

        voice_client.resume()
        await interaction.response.send_message("▶️ Resumed the song.")
        logging.info(f'Resumed music in guild {interaction.guild.id}')

    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="leave",
        description="Make the bot leave the voice channel."
    )
    async def leave(self, interaction: discord.Interaction):
        """Makes the bot leave the voice channel."""
        voice_client = self.voice_clients.get(interaction.guild.id)

        if not voice_client or not voice_client.is_connected():
            await interaction.response.send_message("🔴 I am not connected to any voice channel.", ephemeral=True)
            return

        voice_client.stop()
        await voice_client.disconnect()
        del self.voice_clients[interaction.guild.id]
        del self.music_queues[interaction.guild.id]
        await interaction.response.send_message("👋 Disconnected from the voice channel.")
        logging.info(f'Disconnected from voice channel in guild {interaction.guild.id}')

    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="skip",
        description="Skip the currently playing song."
    )
    async def skip(self, interaction: discord.Interaction):
        """Skips the currently playing song and plays the next one in the queue."""
        voice_client = self.voice_clients.get(interaction.guild.id)

        if not voice_client or not voice_client.is_playing():
            await interaction.response.send_message("🔴 No song is currently playing.", ephemeral=True)
            return

        voice_client.stop()
        await interaction.response.send_message("⏭️ Skipped the current song.", ephemeral=True)
        logging.info(f'Skipped song in guild {interaction.guild.id}')

    def play_next(self, guild_id, error):
        """Plays the next song in the queue."""
        if error:
            logging.error(f'Player error: {error}')
            return

        if self.music_queues[guild_id]:
            next_song = self.music_queues[guild_id].pop(0)
            loop = asyncio.get_event_loop()
            loop.create_task(self.play_song(guild_id, next_song))
        else:
            loop = asyncio.get_event_loop()
            loop.create_task(self.disconnect(guild_id))

    async def play_song(self, guild_id, song):
        """Helper method to play a song from the queue."""
        voice_client = self.voice_clients.get(guild_id)
        if not voice_client:
            return

        try:
            source = await YTDLSource.from_url(song, loop=self.bot.loop, stream=True)
            voice_client.play(source, after=lambda e: self.play_next(guild_id, e))
            channel = self.bot.get_channel(self.bot.config['welcome_channel_id'])  # Or specify a music channel
            if channel:
                await channel.send(f"🎶 Now playing: **{source.title}**")
            logging.info(f'Playing {source.title} in guild {guild_id}')
        except Exception as e:
            logging.error(f"Error playing song: {e}")

    async def disconnect(self, guild_id):
        """Disconnects the bot from the voice channel when the queue is empty."""
        voice_client = self.voice_clients.get(guild_id)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            del self.voice_clients[guild_id]
            del self.music_queues[guild_id]
            logging.info(f'Disconnected from voice channel in guild {guild_id} after queue completion.')


            
    
    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="queue",
        description="Display the current music queue."
    )
    async def queue(self, interaction: discord.Interaction):
        """Displays the current music queue."""
        queue = self.music_queues.get(interaction.guild.id, [])
        if not queue:
            await interaction.response.send_message("📭 The queue is currently empty.", ephemeral=True)
            return

        queue_display = "\n".join([f"{idx + 1}. {song}" for idx, song in enumerate(queue)])
        embed = discord.Embed(title="Music Queue", description=queue_display, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logging.info(f'Displayed queue for guild {interaction.guild.id}')
        
    @app_commands.guilds(GUILD_ID)
    @app_commands.command(
        name="volume",
        description="Adjust the playback volume."
    )
    @app_commands.describe(volume="The desired volume level (0-100).")
    async def volume(self, interaction: discord.Interaction, volume: int):
        """Adjusts the playback volume."""
        if volume < 0 or volume > 100:
            await interaction.response.send_message("🔴 Volume must be between 0 and 100.", ephemeral=True)
            return

        voice_client = self.voice_clients.get(interaction.guild.id)
        if not voice_client or not voice_client.is_playing():
            await interaction.response.send_message("🔴 No music is currently playing.", ephemeral=True)
            return

        voice_client.source.volume = volume / 100
        await interaction.response.send_message(f"🔊 Volume set to {volume}%.")
        logging.info(f'Volume set to {volume}% in guild {interaction.guild.id}')


            

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
    logging.info("Music Cog has been added to the bot.")
    
