# Import library
import discord
import urllib.request, json
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
from discord.ext.commands import bot
from discord.ext import commands
import re
import os
from os import path

import numpy as np






#reads in token from .txt file
token = open("token.txt", "r").read()
client = discord.Client()

#reads in source data from .txt file
file1 = open("datastorage.txt","r+")
content = file1.read()
file1.close()

#function for organizing data
def statsgrabber(country):
    country = specialcases(country)
    countrycap = capitalize(country)
    data = json.loads(content)
    #tests to see if data exits for entered country
    try:
        data[countrycap]
        return (data[countrycap][-1]["confirmed"], data[countrycap][-1]["deaths"], data[countrycap][-1]["recovered"])
    except:
        return "Invalid"

#function for formatting diplayed message
def formatter(country, stats):
    country = specialcases(country)
    countrycap = capitalize(country)
    #toggles upon no data for country
    if stats == "Invalid":
        output = "No statistics for " + countrycap + "."
    else:
        output = "Country: {0}\nConfirmed: {1}\nDeaths: {2}\nRecovered: {3}\n".format(countrycap, "{:,}".format(stats[0]),"{:,}".format(stats[1]),"{:,}".format(stats[2]))
    return output

#function that ignores capitalization of specific characters
def title_except(s, exceptions):
    word_list = re.split(' ', s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

#function to format for .json file
def capitalize(input):
    #ignores special case
    if input == "us":
        output = "US"
    else:
        articles = ['and','of','the']
        output = title_except(input, articles)
    return output

#function for dealing with special cases of country names
def specialcases(input):
    if input == "south korea":
        output = "Korea, South"
    elif input == "united states":
        output = "us"
    elif input == "uk":
        output = "united kingdom"
    else:
        output = input
    return output

#function for plotting data
def plotter(format,country):
    #initializes arrays
    dates = []
    confirms = []
    deaths = []
    recovers = []
    #checks for special cases
    country = specialcases(country)
    #formats for .json file
    countrycap = capitalize(country)
    #loads content
    data = json.loads(content)
    #sees if country exists
    try:
        
        length = len(data[countrycap])
        #populates arrays
        for x in range(0,length):

            date = data[countrycap][x]["date"]
            dates.append(date)

            confirm = data[countrycap][x]["confirmed"]
            confirms.append(confirm)

            death = data[countrycap][x]["deaths"]
            deaths.append(death)

            recover = data[countrycap][x]["recovered"]
            recovers.append(recover)

        #clears out old data 
        plt.clf()

        fig, ax1 = plt.subplots()

        


        #plots data for last 30 days
        if format == "last30":
            #converts data in date format for last 30 days
            xaxisdates = mdates.num2date(mdates.datestr2num(dates[-30:-1]))
            ax1.plot(xaxisdates,confirms[-30:-1], label = "Currently Infected")
            ax1.plot(xaxisdates,recovers[-30:-1], label = "Recovered")
            ax1.plot(xaxisdates,deaths[-30:-1], label = "Deaths")
            plt.title("coronastatsvirus in " + countrycap + " for the last 30 days")
            #plots data
            fig.autofmt_xdate()
            plt.ylabel("People")
            plt.xlabel("Date")
            plt.grid()
            plt.legend()
            
            #saves plot to .png file
            plt.savefig("plot.png")
        #plots data for total time
        elif format == "total":
            xaxisdates = mdates.num2date(mdates.datestr2num(dates))
            ax1.plot(xaxisdates,confirms, label = "Currently Infected")
            ax1.plot(xaxisdates,recovers, label = "Recovered")
            ax1.plot(xaxisdates,deaths, label = "Deaths")
            plt.title("coronastatsvirus in " + countrycap + " Total")
            #plots data
            #fig.autofmt_xdate()
            #plt.xaxis.set_major_locator(xaxisdates)
            fig.autofmt_xdate()
            plt.ylabel("People")
            plt.xlabel("Date")
            plt.grid()
            plt.legend()
            #saves plot to .png file
            plt.savefig("plot.png")
        else:
            #gets rid of old plot
            os.remove("plot.png")
            return
    #if no data for country exits
    except:
        return


#function for displaying help menu
def helper():
    output = "Commands: \n !coronastats => generates statistics with default country as US \n !coronastats (country) => to generate statistics for given country \n !coronastats plot last30 (country) => Generates plot for last thirty days or since first case for given country \n"
    return output

@client.event
async def on_ready():
    #For debugging
    print("You are connected to Discord")
    #sets bot status
    game = discord.Game("!help for commands")
    await client.change_presence(status=discord.Status.online, activity=game)
    return

#Every message sent will prompt this code to run
@client.event
async def on_message(message): 

    #splits up message
    val = message.content.lower().split(" ")
    #inializes array
    countrycontent = []
    #runs with !help is first value of message
    if val[0] == "!help":
        await message.channel.send(helper())
    #runs default code for !coronastats
    if val[0] == "!coronastats" and len(val) != 1 :
        if val[1] == "plot":       
            if len(val) > 3:
                for i in range(3,len(val)) : 
                    countrycontent.append(val[i]) 
                countrycontent = " ".join(countrycontent)
                plotter(val[2],countrycontent)
                #checks to see if plot exists
                if path.exists('plot.png'):
                    await message.channel.send(file=discord.File('plot.png'))
                else:
                    #if no data is found for entered country 
                    await message.channel.send("No statistics for " + capitalize(countrycontent) + ".")
            #runs default plot code
            else:
                plotter("total","united states")
                await message.channel.send(file=discord.File('plot.png'))
        #prints stats for inputted country
        else:
            for i in range(1,len(val)) : 
                countrycontent.append(val[i]) 
            countrycontent = " ".join(countrycontent)
            await message.channel.send(formatter(countrycontent, statsgrabber(countrycontent)))
    #default data
    elif val[0] == "!coronastats" and len(val) == 1:
        await message.channel.send(formatter("united states", statsgrabber("united states")))
        
    return

client.run(token)