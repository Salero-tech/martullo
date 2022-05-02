import discord
from discord.ext import commands
import json
from stirngfun import insertMsg

TOKEN = 'NzY5Mjk0ODgwMTIzNzgxMTgw.X5M7sA.OuOoCLf5OXTDhlt97DMkx5oBBbs'

#load msg from file
jsonFile = open("msgs.json")
jsonMsgList = json.load(jsonFile)
jsonFile.close()


bot = commands.Bot(command_prefix='?')




@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name +" (" + str(bot.user.id) +")")

@bot.event
async def on_message(message):
    #filter bots
    if message.author == bot.user:
        return
    if message.author.bot: return

    #msg mapping
    for item in jsonMsgList:
        #items
        for trig in item["triggers"]:
            if trig.lower() in message.content.lower():
                resp = item["response"]

                #replacing names etc
                resp = insertMsg(resp, "!name!", message.author.display_name)

                #response
                await message.channel.send(resp)
                return



bot.run(TOKEN)