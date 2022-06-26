import os
import sys
import subprocess
try:
    import discord
    import discord.ext
    from discord.ext import commands
    import git
except:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'python-dotenv'])

    #This fuckery installs the latest version of discord.py for us automatically, because repl wont.
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'discord','--upgrade','git+https://github.com/Rapptz/discord.py'])
    #This makes sure gitpython is installed for our github wiki things
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'gitpython'])
    except Exception as error:
         print(error)

import data
import json
import selfupdater
from dotenv import load_dotenv
intents=discord.Intents.all()
directory=data.directory
jsonFile=data.jsonFile
cogFile=data.cogFile
global cogs
#this doesnt work on windows.
if not sys.platform.startswith('win'):
    selfupdater.selfupdate()
client = commands.Bot(command_prefix = 'r.',intents=intents,case_insensitive=True) 

load_dotenv()
    

@client.event
async def on_ready():
    #Just inform the admin of some basic info.
    print(f"Current directory: {directory}")
    print(f"JSON data file: {jsonFile}")
    print(f"Cog JSON data file: {cogFile}")

    #Do any file setup that may be needed
    if(not os.path.exists(jsonFile)):
      with open(jsonFile,'w') as file:
        json.dump({},file)
    if(not os.path.exists(cogFile)):
      with open(cogFile,"w") as file:
        json.dump({},file)

    #This is loaded as it's own item so it cannot accidentally be removed.
    await client.load_extension('debug')
    with open(cogFile,"r") as file:
      cogs = json.load(file)

    #Load all modules
    for cog in cogs:
        if(os.path.exists(cog)):
            await client.load_extension(cogs[cog])
            print(f"Loading cog: {cogs[cog]}")
    print(f"logged in as {client.user}") 
    


client.run(os.getenv("TOKEN"))
