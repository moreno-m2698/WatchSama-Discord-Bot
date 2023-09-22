import os
import time

import discord
from discord.ext import commands

import watchsama
#----------------------------------------------------------------------------------
print('''
     __      __         __         .__                _________                      
    /  \    /  \_____ _/  |_  ____ |  |__            /   _____/____    _____ _____   
    \   \/\/   /\__  \\\   __\/ ___\|  |  \   ______  \_____  \\\__  \  /     \\\__  \  
     \        /  / __ \|  | \  \___|   Y  \ /_____/  /        \/ __ \|  Y Y  \/ __ \_
      \__/\  /  (____  /__|  \___  >___|  /         /_______  (____  /__|_|  (____  /
           \/        \/          \/     \/                  \/     \/      \/     \/ 
       by keopi#4078 |
    ''')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
app_config = watchsama.config.App_Config


@bot.event
async def on_ready() -> None:

    bot_commands = watchsama.bot_commands.__init__
    bot_cogs = watchsama.cogs.mal.MAL.cog_setup
    allowed_cache_size_check = [0, 2]
    testing_output = bot.get_guild(app_config.my_guild()).text_channels[0].send

    print("Connected to discord API")
    
    bot_commands(bot)
    await bot_cogs(bot)

    #TODO: Research alternatives for caching
    # cache_file = os.stat('watchsama/cogs/mal/JSON/anime_complete_data.json').st_size
    # if cache_file == allowed_cache_size_check[0] or cache_file == allowed_cache_size_check[1]:
    #     watchsama.cogs.mal.API.MALSelenium.cache_anime_meta()
    #     print("Creating embeds json")

    await testing_output('Watch-sama is running') #Find out how to get her to talk properly

    await bot.change_presence(status = discord.Status.online)

try:
    bot.run(app_config.bot_token())

except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    time.sleep(5)
    exit(1)


