import os
import time

import discord
from discord.ext import commands

import watchsama.config
import watchsama.cogs.cmds
import watchsama.cogs.mal.MAL
import watchsama.cogs.mal.API.MALSeleniumWrapper

# from watchsama.cogs.mal.MAL import setup
# from watchsama.cogs.mal.API.MALSeleniumWrapper import cache_anime_embeds


#TODO: Choicing random anime feature
#Add timeout
#Add description to first <br>

#Create a view to interact with embed
#Needs to have a single track reroll thats tracked with date
#Should I synthesize or make from a cached list
#----------------------------------------------------------------------------------
print('''
     __      __         __         .__                _________                      
    /  \    /  \_____ _/  |_  ____ |  |__            /   _____/____    _____ _____   
    \   \/\/   /\__  \\   __\/ ___\|  |  \   ______  \_____  \\__  \  /     \\__  \  
     \        /  / __ \|  | \  \___|   Y  \ /_____/  /        \/ __ \|  Y Y  \/ __ \_
      \__/\  /  (____  /__|  \___  >___|  /         /_______  (____  /__|_|  (____  /
           \/        \/          \/     \/                  \/     \/      \/     \/ 
       by keopi#4078 |
    ''')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    print("Connected to discord API")
    watchsama.cogs.cmds.__init__(bot)
    watchsama.cogs.mal.MAL.setup(bot)

    #TODO: find a way to cache the range so u dont wanna die

    check_file = os.stat('watchsama/cogs/mal/anime_embed.json').st_size
    if check_file == 0 or check_file == 2:
        watchsama.cogs.mal.API.MalSeleniumWrapper.cache_anime_embeds()
        print("populating json")
    await bot.guilds[0].text_channels[0].send('Watch-sama is running') #Find out how to get her to talk properly

    await bot.change_presence(status = discord.Status.online)



#TODO: ADD TO ENV VARIABLE
try:

    bot.run(watchsama.config.bot_token())

except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    time.sleep(5)
    exit(1)