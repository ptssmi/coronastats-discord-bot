# Import libraries
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
import csv
import numpy as np

#reads in token from .txt file
token = open("token.txt", "r").read()
client = discord.Client()

#opens .txt file containing country data and populates it into the program
def fileread():
    #reads in source data from .txt file
    file1 = open("datastorage.txt","r+")
    content = file1.read()
    file1.close()
    return content

#reads in data from file and filters dependent on inputted county and state
def csvcountyread(county,state):
    with open('countydata.txt', 'r') as file2:
        reader = csv.reader(file2)
        state = capitalize(state)
        county = capitalize(county)
        for row in reversed(list(reader)):
            date = str(row[0])
            if row[0] == date:
                if row[1] == county:
                    if row[2] == state:
                            cases = int(row[4])
                            deaths = int(row[5])
                            return "State: " + state + "\n" + "County: " + county + "\n" + "Total Cases: " + format (cases, ',d') + "\n" + "Deaths: " + format (deaths, ',d')

#reads in data from state file and filters dependent on inputted state
def csvstateread(state):
    with open('statedata.txt', 'r') as file3:
        reader = csv.reader(file3)
        state = capitalize(state)
        for row in reversed(list(reader)):
            date = str(row[0])
            if row[0] == date:
                if row[1] == state:
                    cases = int(row[3])
                    deaths = int(row[4])
                    return "State: " + state + "\n" + "Total Cases: " + format (cases, ',d') + "\n" + "Deaths: " + format (deaths, ',d')

#plots data dpending on which state is inputted
def csvstateplot(state):
    with open('statedata.txt', 'r') as file3:
        dates = []
        cases = []
        deaths = []
        reader = csv.reader(file3)
        state = capitalize(state)
        #finds the inputted state data
        for row in list(reader):
                if row[1] == state:
                    date = row[0]
                    dates.append(date)
                    case = row[3]
                    cases.append(case)
                    death = row[4]
                    deaths.append(death)
        #case for if an invalid state is entered
        if cases == []:
            if path.exists('plot.png'):
                os.remove("plot.png")
                return
            else:
                return
        else:
            
            try:
                #converts list of strings to list of ints
                cases = list(map(int, cases))
                deaths = list(map(int, deaths))
                dates = mdates.num2date(mdates.datestr2num(dates[-30:]))
                #clears out old data 
                plt.clf()
                fig, ax1 = plt.subplots()
                #plots data
                ax1.plot(dates,cases[-30:], label = "Infected")
                ax1.plot(dates,deaths[-30:], label = "Deaths")
                plt.title("Coronavirus in " + state + " for the last 30 days")
                fig.autofmt_xdate()
                plt.ylabel("People")
                plt.xlabel("Date")
                plt.grid()
                plt.legend()
                #saves plot to .png file
                plt.savefig("plot.png")
                plt.close()
            except:
                try:
                    os.remove("plot.png")
                    return
                except:
                    return

#plots data depending on county and state inputted
def csvcountyplot(county,state):
    with open('countydata.txt', 'r') as file3:
        dates = []
        cases = []
        deaths = []
        reader = csv.reader(file3)
        state = capitalize(state)
        county = capitalize(county)
        #finds the inputted county and state data
        for row in list(reader):
               if row[1] == county:
                    if row[2] == state:
                        date = row[0]
                        dates.append(date)
                        case = row[4]
                        cases.append(case)
                        death = row[5]
                        deaths.append(death)
                        
        #case for if an invalid state is entered
        if cases == []:
            if path.exists('plot.png'):
                os.remove("plot.png")
                return
            else:
                return
        else:
            
            try:
                #converts list of strings to list of ints
                cases = list(map(int, cases))
                deaths = list(map(int, deaths))
                dates = mdates.num2date(mdates.datestr2num(dates[-30:]))
                #clears out old data 
                plt.clf()
                fig, ax1 = plt.subplots()
                #plots data
                ax1.plot(dates,cases[-30:], label = "Infected")
                ax1.plot(dates,deaths[-30:], label = "Deaths")
                plt.title("Coronavirus in " + county + " County " + state + " for the last 30 days")
                fig.autofmt_xdate()
                plt.ylabel("People")
                plt.xlabel("Date")
                plt.grid()
                plt.legend()
                #saves plot to .png file
                plt.savefig("plot.png")
                plt.close()
            except:
                try:
                    os.remove("plot.png")
                    return
                except:
                    return

#function for organizing data for discord output
def statsgrabber(country):
    country = specialcases(country)
    countrycap = capitalize(country)
    data = json.loads(fileread())
    #tests to see if data exits for entered country
    try:
        data[countrycap]
        return (data[countrycap][-1]["confirmed"], data[countrycap][-1]["deaths"], data[countrycap][-1]["recovered"])
    except:
        return "Invalid"

#function for retreiving Univeristy of Cincinnati data
def ucstatgrabber():
    f = open("ucdata.txt", "r")
    return f.read()

#function for formatting diplayed message
def formatter(country, stats):
    country = specialcases(country)
    countrycap = capitalize(country)
    #toggles upon no data for country
    if stats == "Invalid":
        output = "No statistics for " + countrycap + "."
    else:
        output = "{0}\nConfirmed: {1}\nDeaths: {2}\nRecovered: {3}\n".format(countrycap, "{:,}".format(stats[0]),"{:,}".format(stats[1]),"{:,}".format(stats[2]))
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
def plotter(country):
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
    data = json.loads(fileread())
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

        #converts data in date format for last 30 days
        xaxisdates = mdates.num2date(mdates.datestr2num(dates[-30:]))
        ax1.plot(xaxisdates,confirms[-30:], label = "Infected")
        ax1.plot(xaxisdates,recovers[-30:], label = "Recovered")
        ax1.plot(xaxisdates,deaths[-30:], label = "Deaths")
        plt.title("Coronavirus in " + countrycap + " for the last 30 days")
        #plots data
        fig.autofmt_xdate()
        plt.ylabel("People")
        plt.xlabel("Date")
        plt.grid()
        plt.legend()  
        #saves plot to .png file
        plt.savefig("plot.png")
        plt.close()

    #if no data for country exits
    except:
        try:
            os.remove("plot.png")
            return
        except:
            return


#function for displaying help menu
def helper():
    output = "**Commands:** ```!coronastats => generates statistics with default country as US``````!coronastats uc => generates statistics for The University of Cincinnati``````!coronastats (country) => generates statistics for given country``````!coronastats state (state) => generates statistics for given state``````!coronastats state plot (state) => generates a plot of the last thirty days for the``````!coronastats county (county) (state) => generates statistics for the given county and state``````!coronastats county plot (county) (state) => generates plot for the last thirty days of the given county and state``````!coronastats plot => generates plot of last thirty days with default country as US``````!coronastats plot (country) => generates plot for last thirty days for the given country```"
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
    statecontent = []
    #runs with !help is first value of message
    if val[0] == "!help":
        await message.channel.send(helper())
    #runs default code for !coronastats
    if val[0] == "!coronastats" and len(val) != 1 :
        if val[1] == "plot":       
            if len(val) > 2:
                for i in range(2,len(val)) : 
                    countrycontent.append(val[i]) 
                countrycontent = " ".join(countrycontent)
                plotter(countrycontent)
                #checks to see if plot exists
                if path.exists('plot.png'):
                    await message.channel.send(file=discord.File('plot.png'))
                else:
                    #if no data is found for entered country 
                    await message.channel.send("No statistics for " + capitalize(countrycontent) + ".")
            #runs default plot code
            else:
                plotter("united states")
                await message.channel.send(file=discord.File('plot.png'))
        elif val[1] == "county":
            if val[2] == "plot":
                #case for if state is one word
                if len(val) == 5:
                    csvcountyplot(val[3],val[4])
                    #checks to see if plot has been created
                    if path.exists('plot.png'):
                        await message.channel.send(file=discord.File('plot.png'))
                    else:
                    #if no data is found for entered country 
                        await message.channel.send("No statistics for " + capitalize(val[3]) + ".")
                #case for if state is more than one word
                elif len(val) > 5:
                    for i in range(4,len(val)):
                        statecontent.append(val[i]) 
                    statecontent = " ".join(statecontent)
                    csvcountyplot(val[3],statecontent)
                    #checks to see if plot has been created
                    if path.exists('plot.png'):
                        await message.channel.send(file=discord.File('plot.png'))
                    else:
                        await message.channel.send("Please enter a valid state.")
            #command for printing county data
            else:
                #case for if state is one word
                if len(val) == 4:
                    try:
                        await message.channel.send(csvcountyread(val[2],val[3]))
                    except:
                        await message.channel.send("Please enter a valid county and state.")
                #case for if state is more than one word
                elif len(val) > 4:
                    for i in range(3,len(val)) : 
                        statecontent.append(val[i]) 
                    statecontent = " ".join(statecontent)
                    #checks to see if inputted county and state are valid
                    try:
                        await message.channel.send(csvcountyread(val[2],statecontent))
                    except:
                        await message.channel.send("Please enter a valid county and state.")
        #command for retrieving state data
        elif val[1] == "state":
            #command for plotting state data
            if val[2] == "plot":
                #case for if the state is one word
                if len(val) == 4:
                    csvstateplot(val[3])
                    #checks to see if a plot has been generated
                    if path.exists('plot.png'):
                        await message.channel.send(file=discord.File('plot.png'))
                    else:
                    #if no data is found for entered country 
                        await message.channel.send("No statistics for " + capitalize(val[3]) + ".")
                #case for if the state is more than one word
                elif len(val) > 4:
                    for i in range(3,len(val)):
                        statecontent.append(val[i]) 
                    statecontent = " ".join(statecontent)
                    csvstateplot(statecontent)
                    if path.exists('plot.png'):
                        await message.channel.send(file=discord.File('plot.png'))
                    else:
                        await message.channel.send("Please enter a valid state.")
            #case for outputted state information
            else:
                #case for if state is one word
                if len(val) == 3:
                    #checks to see if inputted state is valid
                    try:
                        await message.channel.send(csvstateread(val[2]))
                    except:
                        await message.channel.send("Please enter a valid state.")
                #case for if state is more than one word
                elif len(val) > 3:
                    for i in range(2,len(val)):
                        statecontent.append(val[i]) 
                    statecontent = " ".join(statecontent)
                    try:
                        await message.channel.send(csvstateread(statecontent))
                    except:
                        await message.channel.send("Please enter a valid state.")
        elif val[1] == 'uc':
            await message.channel.send("**University of Cincinnati Cases: **" +  ucstatgrabber())
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