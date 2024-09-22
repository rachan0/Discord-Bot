import discord
import json

with open('token.json', 'r') as f:
    YOUR_TOKEN = json.load(f)['token']

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('Hello'):
            await message.channel.send(f'Hi there! {message.author}')
        
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(YOUR_TOKEN)
