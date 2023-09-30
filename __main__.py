import os
import time
from typing import Any, List, Mapping, Optional

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group, Callable


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

class MyHelpCommand(commands.HelpCommand):
    
    def __init__(self) -> None:
        super().__init__()
    
    async def send_bot_help(self, mapping: Mapping[Cog | None, List[Command[Any, Callable[..., Any], Any]]]) -> None:
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
        

    async def send_cog_help(self, cog: Cog) -> None:
        await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
     
    async def send_group_help(self, group: Group[Any, Callable[..., Any], Any]) -> None:
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')
    
    async def send_command_help(self, command: Command[Any, Callable[..., Any], Any]) -> None:
        await self.get_destination().send(command.name)

class WatchSama(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = intents,
            help_command=MyHelpCommand()
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

    embed = watchsama.tools.WatchSamaEmbed(title="WatchSama Bot Info", description = "Thank you for choosing to use WatchSama!")
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


