"""
SD Hacks 2021
Authors: Garvin Mo Zhen, Jason Leong, Brian Che
Description: Discord Bot that Alerts Users Class Times
"""

# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import sqlite3
from sqlite3 import Error

def create_db(file):
    conn = None
    try:
        conn = sqlite3.connect(file)
        print (sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


file = r"ClassReminderBot.db"
create_db(file)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='AddClass', help='Add Class to your Reminder Bot')
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

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

bot.run(TOKEN)
