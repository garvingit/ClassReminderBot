"""
SD Hacks 2021
Authors: Garvin Mo Zhen, Jason Leong, Brian Che
Description: Discord Bot that Alerts Users Class Times
"""

# bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    help_menu = [
        '!Add_Class <Name of Class> <Time>'
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content == '!help':
        response = help_menu
        await message.channel.send(response)

    if message.content.startswith('!add'):
            

client.run(TOKEN)