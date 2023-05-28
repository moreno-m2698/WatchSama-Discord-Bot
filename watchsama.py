import os

import discord
from discord.ext import commands

from watchsama.config import bot_token
from watchsama.cogs.mal.MAL import setup
from watchsama.cogs.mal.API.MALSeleniumWrapper import cache_anime_embeds


#---------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
#-------------------------------------------------------------------------

#TODO: Choicing random anime feature
#Add timeout
#Add description to first <br>

#Create a view to interact with embed
#Needs to have a single track reroll thats tracked with date
#Should I synthesize or make from a cached list
#----------------------------------------------------------------------------------

@bot.event
async def on_ready() -> None:
    print('''
     __      __         __         .__                _________                      
    /  \    /  \_____ _/  |_  ____ |  |__            /   _____/____    _____ _____   
    \   \/\/   /\__  \\   __\/ ___\|  |  \   ______  \_____  \\__  \  /     \\__  \  
     \        /  / __ \|  | \  \___|   Y  \ /_____/  /        \/ __ \|  Y Y  \/ __ \_
      \__/\  /  (____  /__|  \___  >___|  /         /_______  (____  /__|_|  (____  /
           \/        \/          \/     \/                  \/     \/      \/     \/ 
       by keopi#4078 |
    ''')
    setup(bot)

    #TODO: find a way to cache the range so u dont wanna die

    check_file = os.stat('watchsama/cogs/mal/anime_embed.json').st_size
    if check_file == 0 or check_file == 2:
        cache_anime_embeds()
        print("populating json")
    await bot.guilds[0].text_channels[0].send('Watch-sama is running') #Find out how to get her to talk properly

@bot.command()
async def stop(ctx: commands.Context) -> discord.Message:
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await bot.close()


#TODO: ADD TO ENV VARIABLE
bot.run(bot_token())