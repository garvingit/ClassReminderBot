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

@bot.command(name='addclass', help='Add Class to your Reminder Bot')
async def on_message(message, className, start, end, days):
    #when the bot types this command, do nothing
    if message.author == bot.user:
        return

    await message.channel.send('You passed {}, {}, {}, {}'.format(className, start, end, days))

# Bot announces hello every 10 seconds
@tasks.loop(seconds=10)
async def test():
    channel = bot.get_channel(812874796018696215)
    await channel.send('hello')

bot.run(TOKEN)
