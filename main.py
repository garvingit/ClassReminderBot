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

def create_table(file, table_name):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS class_table
        (
            className varchar(255) PRIMARY KEY NOT NULL,
            classStartTime varchar(7),
            classEndTime varchar(7),
            classdays varchar(5)
        )
    """)
    conn.commit()
    conn.close()

file = r"ClassReminderBot.db"
table_name = 'Class'
create_db(file)
create_table(file, table_name)



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='Add_Class', help='Add Class to your Reminder Bot')
async def on_message(message):
    if message.author == bot.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await message.channel.send(response)

bot.run(TOKEN)
