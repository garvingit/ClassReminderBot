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
    """
    read the database line by line, currently prints the data should return it!!!! 
    """
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

def remove_classes(conn, className):
    c = conn.cursor()
    c.execute("DELETE FROM class_table WHERE className = '{0}'".format(
        className
    )) 
    conn.commit()
    

def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_day = datetime.today().weekday()
    return ("Current Time: ", current_time, current_day)


def main():
    file = r"ClassReminderBot.db"
    table_name = 'Class'

    conn = sqlite3.connect(file)

    #add_classes(conn, "COMP137", "3:00pm", "5:00pm", "MWF")            // TESTING 
    #read_classes(conn)                                                 // TESTING 
    
    #remove_classes(conn, 'COMP163')                                    // TESTING 

    read_classes(conn)
    #create_db(file)                        // Creates database file 
    #create_table(file, table_name)         // Creates table within database

    getTime()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = commands.Bot(command_prefix = '!')

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        test.start()

    # Bot announces hello every 10 seconds
    @tasks.loop(minutes=1)
    async def test():
        channel = bot.get_channel(812874796018696215)
       
        await channel.send(getTime())


    @bot.command(name='addclass', help='<classname> <8:00am> <9:15am> <MWF>')
    async def on_message(message, className, classStartTime, classEndTime, classDays):
    #when the bot types this command, do nothing
        if message.author == bot.user:
            return

        #splits in the time 3:00pm to an array ["3", "00pm"]
        formattedStart = formatTime(classStartTime)
        formattedEnd = formatTime(classEndTime)

        weekday = {"m": "0", "t": "1", "w": "2", "th": "3", "f": "4"}

        classDays = classDays.lower()
        formattedDays = ""
        for day in weekday:
            if day == "t":
                if classDays.count(day) == 2 or day in classDays:
                    formattedDays += weekday[day]
            else:
                if day in classDays:
                    formattedDays += weekday[day]
        
        #adding the classes to databse
        add_classes(conn, className, formattedStart, formattedEnd, formattedDays)

        read_classes(conn)## CAN DELETE THIS LINE JUST PRINTING OUT THE CLASSES TO SEE

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
