# Import library
import discord

#Reads in personal discord bot token
token = open("token.txt", "r").read()

client = discord.Client()

#For debugging
@client.event
async def on_ready():
    print("You are connected to Discord")

#Every message sent will prompt this code to run
@client.event
async def on_message(message): 
    #Opens .txt file that is storing data
    data = open("datastorage.txt","r+")
    output = data.read()
    data.close()
    #If this keyword is sent in discord then the stats will be sent to that channel
    if "!coronastats" in message.content.lower():
	    await message.channel.send(output)
        
client.run(token)