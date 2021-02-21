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
    classes = []
    for row in class_list:
        classes.append(row)
    return classes

def print_classes(conn):
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
    return [current_time, current_day]




def main():
    file = r"ClassReminderBot.db"
    table_name = 'Class'

    create_db(file)                        # Creates database file 
    create_table(file, table_name)         # Creates table within database

    conn = sqlite3.connect(file)

    #add_classes(conn, "COMP137", "3:00pm", "5:00pm", "MWF")            // TESTING 
    #read_classes(conn)                                                 // TESTING 
    
    #remove_classes(conn, 'COMP163')                                    // TESTING 

    print_classes(conn)

    getTime()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = commands.Bot(command_prefix = '!')

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        remindClass.start()

    # Bot announces hello every 10 seconds
    @tasks.loop(seconds=30)
    async def remindClass():
        channel = bot.get_channel(812874796018696215)
        currentTime = getTime()[0]
        currentDay = getTime()[1]
        classRows = read_classes(conn)
        
        for className in classRows:
            # string format ("15:00")
            classTime = className[1].split(":")

            # string format ("024")
            classDay = className[3]

            name = className[0]
            
            classHour = classTime[0]
            classMinute = classTime[1]

            if int(classMinute) >= 10:
                tenMinBefore = '0' + str(classHour) + ':0' + str(int(classMinute) - 10)
            else:
                tenMinBefore = str(int(classHour) - 1) + ':' + str(int(classMinute) + 50)

            if int(classMinute) >= 5:
                fiveMinBefore = '0' + str(classHour) + ':' + str(int(classMinute) - 5)
            else:
                fiveMinBefore = str(int(classHour) - 1) + ':' + str(int(classMinute) + 55)

            if str(currentDay) in classDay:
                print("ClassName: {}".format(name))
                print("Current Time is: {}, 10minbefore: {}".format(currentTime, tenMinBefore))
                print("Current Time is: {}, 5minbefore: {}".format(currentTime, fiveMinBefore))
                print("Current Time is equal to 10minbeforeclass: {}".format(currentTime == tenMinBefore))
                print("Current Time is equal to 10minbeforeclass: {}".format(currentTime == fiveMinBefore))
                print("currentime type: ".format(type(currentTime) is str))
                print("fiveminbefore type: ".format(type(fiveMinBefore) is str))
                if currentTime == tenMinBefore:
                    await channel.send(name + " STARTS IN TEN MINUTES!")
                if currentTime == fiveMinBefore:
                    await channel.send(name + " STARTS IN FIVE MINUTES!!!")
                if currentTime == classTime[1]:
                    await channel.send(name + " STARTS RIGHT NOW!!!!!")


        #await channel.send(currentDay)


    @bot.command(name='addclass', help='<classname> <8:00am> <9:15am> <MWF>')
    async def on_message(message, className, classStartTime, classEndTime, classDays):
    #when the bot types this command, do nothing
        if message.author == bot.user:
            return

        #splits in the time 3:00pm to an array ["3", "00pm"]
        formattedStart = formatTime(classStartTime)
        formattedEnd = formatTime(classEndTime)

        weekday = {"m": "0", "t": "1", "w": "2", "th": "3", "f": "4", "s": "6"}

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

    @bot.command(name='removeclass', help='<classname> <8:00am> <9:15am> <MWF>')
    async def on_message(message, className):
    #when the bot types this command, do nothing
        if message.author == bot.user:
            return

        channel = bot.get_channel(812874796018696215)
        mention = message.author.mention
        await channel.send(f"Deleted %s for {mention}" % className)
        remove_classes(conn, className)

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
