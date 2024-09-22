import discord
import json

with open('token.json', 'r') as f:
    YOUR_TOKEN = json.load(f)['token']

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(YOUR_TOKEN)
