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

intents = discord.Intents.default()
intents.message_content = True

class WatchSama(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = intents
        )

    async def setup_hook(self) -> None:
        
        #NOTE: selenium will  not enable me to allow for MAL slash commands atm. Might need to look at threading package
        #REFERENCE: https://www.youtube.com/watch?v=U0Us5NHG-nY for slash commands and cogs

        await self.load_extension(f"watchsama.cogs.mal.MAL")
        




bot = WatchSama()
app_config = watchsama.config.App_Config


@bot.event
async def on_ready() -> None:

    

    dev_guild = bot.get_guild(app_config.my_guild()).text_channels[0].send

    watchsama.cogs.general.__init__(bot)
    
    print("Connected to discord API")


    await dev_guild('WatchSama is running')
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


