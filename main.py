"""
SD Hacks 2021
Authors: Garvin Mo Zhen, Jason Leong, Brian Che
Description: Discord Bot that Alerts Users Class Times
"""

# bot.py
import os
import random

import discord
from discord.ext import commands, tasks
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
            classDays varchar(5)
        )
    """)
    conn.commit()
    conn.close()

def read_classes(conn):
    c = conn.cursor()
    class_list = c.execute("SELECT * FROM class_table")
    for row in class_list:
        print (row)
    
def add_classes(conn, className, classStartTime, classEndTime, classDays):
    c = conn.cursor()
    c.execute("INSERT INTO class_table VALUES ('{0}', '{1}', '{2}', '{3}')".format(
        className, classStartTime, classEndTime, classDays
    ))
    conn.commit()

def main():
    file = r"ClassReminderBot.db"
    table_name = 'Class'

    conn = sqlite3.connect(file)

    add_classes(conn, "COMP137", "3:00pm", "5:00pm", "MWF")
    read_classes(conn)

    conn.close()

    #create_db(file)
    #create_table(file, table_name)

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


if __name__ == '__main__':
    main()