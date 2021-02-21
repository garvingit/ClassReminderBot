"""
SD Hacks 2021
Authors: Garvin Mo Zhen, Jason Leong, Brian Che
Description: Discord Bot that Alerts Users Class Times
"""

# bot.py
import os
import random
import datetime

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import sqlite3
from sqlite3 import Error

from datetime import datetime 

bot = None
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

def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print("Current Time: ", current_time)


def main():
    file = r"ClassReminderBot.db"
    table_name = 'Class'

    conn = sqlite3.connect(file)

    #add_classes(conn, "COMP137", "3:00pm", "5:00pm", "MWF")
    read_classes(conn)

    #create_db(file)
    #create_table(file, table_name)

    getTime()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = commands.Bot(command_prefix = '!')

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    # Bot announces hello every 10 seconds
    @tasks.loop(seconds=10)
    async def test():
        channel = bot.get_channel(812874796018696215)
        await channel.send('hello')

    @bot.command(name='addclass', help='Add Class to your Reminder Bot')
    async def on_message(message, className, start, end, days):
    #when the bot types this command, do nothing
        if message.author == bot.user:
            return

        #splits in the time 3:00pm to an array ["3", "00pm"]
        formattedStart = formatTime(start)
        formattedEnd = formatTime(end)

        add_classes(conn,className, formattedStart, formattedEnd, days)
        read_classes(conn)

    bot.run(TOKEN)

    conn.close()

def formatTime(time):
    """
    input: time would be a string like "3:00pm", "10:00am"
    an array like ["3", "00", "pm"] and ["10", "00", "am"] would be processed
    
    return: 3:00pm would be return in a 24hr format to 15:00
    """
    #splits in the time 3:00pm to an array ["3", "00pm"]
    timeSplit = time.split(":")
    timeSplit.append(timeSplit[1][-2:])
    timeSplit[1] = timeSplit[1][:-2]
    realtime = ""

    if timeSplit[2] == "pm":
        realtime = str(int(timeSplit[0]) + 12)
        realtime = realtime + ":" + timeSplit[1]
    else:
        """ otherwise its am"""
        realtime = ':'.join(timeSplit[time] for time in range(2))
    
    return realtime


if __name__ == '__main__':
    main()
