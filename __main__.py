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
bot = commands.Bot(command_prefix="/", intents=intents)
app_config = watchsama.config.App_Config



@bot.event
async def on_ready() -> None:

    bot_commands = watchsama.bot_commands.__init__
    bot_cogs = watchsama.cogs.mal.MAL.cog_setup
    

    #TODO: get the bot to only spit out to main server if we are wanting to host
    testing_output = bot.get_guild(app_config.my_guild()).text_channels[0].send

    print("Connected to discord API")
    
    bot_commands(bot)
    await bot_cogs(bot)
    await testing_output('WatchSama is running') #Find out how to get her to talk properly
    await bot.change_presence(status = discord.Status.idle)

@bot.event
async def on_guild_join(guild:discord.Guild) -> None:

    embed = watchsama.tools.WatchSamaEmbed(title="WatchSama Bot Info", description = "Thank you for choosing to use WatchSama! To get started, type '/help' to see my commands.")
    await guild.text_channels[0].send(embed=embed)

@bot.event
async def on_guild_remove(guild: discord.Guild) -> None:
    # This should be done for logging/feedback in  a main guild or console
    pass


try:
    bot.run(app_config.bot_token())

except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    time.sleep(5)
    exit(1)


