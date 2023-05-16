# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import random
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#-----------------------------------------------------------------------------------------------------------------------------------------------
mal_username = "gabslittlepogger"
intents = discord.Intents.default()
intents.message_content = True
watchsama = commands.Bot(command_prefix="!", intents=intents)

#------------------------------------------------------------------------------------------------------------------------------------------------

# Add gabs kicking function
# add more cringe dialogue
# Create embed for user interface
# 

#---------------------------------------------------------------------------------------------------------------------------

def create_embed(title: str, description: str):
    cherry_blossom = discord.Color.from_str('#FFB7C5')
    return discord.Embed(colour=cherry_blossom, title=title, description=description)



@watchsama.event
async def on_ready():
    await watchsama.guilds[0].text_channels[0].send('Watch-sama is running')


@watchsama.command()
async def stop(ctx):
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await watchsama.close()
    

@watchsama.command()
async def info(ctx):
    await ctx.send(ctx.author)
    user = await watchsama.fetch_user(ctx.author.id)
    await ctx.send(user.banner)
    

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
   

@watchsama.command()
async def repeat(ctx, *args): 
    #args is stored as a tuple
    repetition = ' '.join(args)
    await ctx.send(repetition)

@watchsama.command()
async def repeat2(ctx, *, arg):
    await ctx.send(arg)

@watchsama.command()
async def currentguild(ctx):
    await ctx.send(ctx.guild.text_channels)



class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'

@watchsama.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


#$-------------------------------------------------------------------------------------------------------------------------

def create_view():
    return discord.ui.View()

@watchsama.command()
async def test(ctx):
    title = 'Anime Night'
    embed = create_embed(title, 'test')
    view =  create_view()
    test_button = discord.ui.Button(label='test')
    view.add_item(test_button)
    await ctx.send(embed = embed, view = view)

@watchsama.command()
async def connection(ctx):
    pass

# hold onto session token from cookies
# shif to selenium





watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')

