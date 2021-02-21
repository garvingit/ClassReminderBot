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

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='addclass', help='Add Class to your Reminder Bot')
async def on_message(message, className, start, end, days):
    #when the bot types this command, do nothing
    if message.author == bot.user:
        return

    await message.channel.send('You passed {}, {}, {}, {}'.format(className, start, end, days))

bot.run(TOKEN)
