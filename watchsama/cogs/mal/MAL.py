

import discord
from discord.ext import commands
from selenium import webdriver

from .API.RawAnimeData import SeleniumRawData, SeleniumSearchData, ExtendedSeleniumRawData
from .API.Embeds import BasicEmbed, ExtendedEmbed

from .API.ui.ViewBuilder import MALViewBuilder
from .API.MALController import MAL_Controller
class MALCog(commands.Cog): #singleton thingy

    ''' Honestly makes more sense for this cog to validate whether or not there is anything in cache'''

    #NOTE: currently We shall assume no caching and will pull the data from MAL
    
    def __init__(self, bot):
        self.bot = bot
        #self.driver = driver

    @commands.command()
    async def watching(self, ctx: commands.Context) -> discord.Message:
        ''' This command will give the user back a discord message that shows some of the shows they are watching'''
        status = 1
        driver = webdriver.Chrome() #canditate to be injected
        print(f"WebDriver: {driver} has been initiated")
        rawData = ExtendedSeleniumRawData.create_Anime_List(driver=driver, status = status)
        chunker = 5
        data_for_view = list(SeleniumRawData.list_chunking(rawData, chunker))
        embeds = [] #can be a method or embeds can be injected
        for anime in data_for_view[0]:
            url = anime['reference']
            title= anime['name']
            media =  anime['media']
            status = anime['status']
            image = anime['image']
            progress= anime['progress']
            description = SeleniumRawData.get_Description(driver, url)
            embed = BasicEmbed(url = url, title = title, media = media, status = status, description = description, image = image)
            embeds.append(embed)
        driver.quit()
        print(f"WebDriver: {driver} is now closed")
        index = 0
        view = MALViewBuilder.create_View(embeds = embeds, data = data_for_view) #create extended
        message: discord.Message = ctx.send(content = f"Progress: {progress}", view = view, embed = embeds[index]) #create extended
        await message


    @commands.command()
    async def complete(self, ctx: commands.Context) -> discord.Message:

        ''' This command will give the user back a discord message that shows what shows they have completed'''

        # TODO: FOLLOW PROPER OBJECT FACTORY CONVENTION

        status = 2
        driver = webdriver.Chrome()
        print("A WebDriver has been initiated")
        rawData = SeleniumRawData.create_Anime_List(driver = driver, status=status)
        chunker = 5
        data_for_view = list(SeleniumRawData.list_chunking(rawData, chunker))
        embeds = []
        for anime in data_for_view[0]:
            url = anime['reference']
            title= anime['name']
            media =  anime['media']
            status = anime['status']
            image = anime['image']
            description = SeleniumRawData.get_Description(driver, url)
            embed = BasicEmbed(url = url, title = title, media = media, status = status, description = description, image = image)
            embeds.append(embed)
        driver.close()
        print("WebDriver is now closed")
        index = 0
        view = MALViewBuilder.create_View(embeds = embeds, data = data_for_view)
        message: discord.Message = ctx.send(content = f"Testing this function:", view = view, embed = embeds[index])
        await message

    @commands.command()
    async def search(self, ctx: commands.Context, *args) -> discord.Message:
        ''' This command will allow user to make a search on MAL and return a list of 5 shows that meet the description'''

        search = '%20'.join(args)
        if len(search) < 3:
            await ctx.send(content = "Your keyword is too short")
        else:
            print("Here is the search string: ", search)
            driver = webdriver.Chrome()
            print("A WebDriver has been initiated")
            url_list = SeleniumSearchData.create_Anime_List(driver=driver, search=search)
            driver.quit()
            print("WebDriver is now closed")
            view = MALViewBuilder.create_Search_View(url_list)

            await ctx.send(content = url_list[0], view = view)

async def cog_setup(bot: commands.Bot):
    await bot.add_cog(MALCog(bot))


#TODO: ADD TIMEOUTS TO VIEWS