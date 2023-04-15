import discord
import asyncio
import json


# Load the config file
with open('config.json', 'r') as f:
    config = json.load(f)

# Get the config values
bot_token = config['bot_token']
discord_channel_id = int(config['discord_channel_id'])
server_ip_address = config['server_ip_address']
server_port = int(config['server_port'])

class DiscordClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.channel.id == discord_channel_id:
            # Send the message to the Valheim server
            reader, writer = await asyncio.open_connection(server_ip_address, server_port)
            writer.write(f"{message.author.name}: {message.content}".encode())
            writer.write_eof()
            await writer.drain()
            writer.close()
            

intents = discord.Intents().all()
client = DiscordClient(intents=intents)
client.run(bot_token)
