import discord
from discord.ext import commands
import json
from stirngfun import insertMsg
import os
import datetime
from os.path import exists


#list for triggers
jsonMsgList = []

#get args
TOKEN = os.environ["TOCKEN"]
PREFIX = os.environ["PREFIX"]
ACTIVITY = os.environ["ACTIVITY"].replace("_", " ")

print(TOKEN)

FILE_PATH = "./data/msgs.json"

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all(), activity=discord.Game(ACTIVITY))

#remove default help command
bot.remove_command("help")

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name +" (" + str(bot.user.id) +")")

@bot.event
async def on_message(message):
    if message.content[:len(PREFIX)] == PREFIX:
        await bot.process_commands(message)
        return
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
                #replacing zeit
                resp = insertMsg(resp, "!zeit!", datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

                #response
                await message.channel.send(resp)
                return


@bot.command()
async def help (ctx):
    msg = ""
    msg += "**list triggers:** ?triggers\r"
    msg += "**add trigger:** ?add [ *trigger1* *trigger2* ] *response*\r"
    msg += "**Special key for response:** !zeit! => time !name! => name\r"
    msg += "**remove trigger:** ?remove *trigger name*\r"
    await ctx.send(msg)

@bot.command()
async def triggers (ctx):
    embed = discord.Embed(title="triggers:")

    triggers = ""
    resp = ""

    for item in jsonMsgList:
        triggers = "`{data}`".format(data=str(item["triggers"]))
        resp = "`{data}`".format(data=item["response"])
        embed.add_field(name=triggers, value=resp)

    await ctx.send(embed=embed)

@bot.command()
async def add (ctx, *args):
    arglist = list(args)
    argString:str = " ".join(arglist)

    triggerStart = argString.index("[")
    triggerEnd = argString.rindex("]")

    triggers = argString[triggerStart+1:triggerEnd].split(" ")
    #clean up
    triggers = list(filter(None, triggers))

    resp = argString[triggerEnd+1:].lstrip()
    

    jsonMsgList.append({
        "triggers": triggers,
        "response": resp
    })

    saveMSG()

    await ctx.send("ADDED")

@bot.command()
async def remove (ctx, trig):
    for i in range(len(jsonMsgList)):
        triggers = jsonMsgList[i]["triggers"]
        if trig in triggers:
            del jsonMsgList[i]
            saveMSG()
            break
    await ctx.send("REMOVED")

def loadMSG ():
    global jsonMsgList
    #load msg from file
    jsonFile = open(FILE_PATH)
    jsonMsgList = json.load(jsonFile)
    jsonFile.close()

def saveMSG ():
    global jsonMsgList
    #load msg from file
    jsonFile = open(FILE_PATH, "w")
    jsonFile.write(json.dumps(jsonMsgList, indent=4))
    jsonFile.close()

def checkIfJsonFileExists():
    if not exists(FILE_PATH):
        jsonFile = open(FILE_PATH, "w")
        jsonFile.write(json.dumps([], indent=4))
        jsonFile.close()

if __name__ == "__main__":
    checkIfJsonFileExists()
    loadMSG()
    bot.run(TOKEN)

