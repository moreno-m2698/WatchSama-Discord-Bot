from discord import ui
from discord.ui import View, Button, Item
from discord import ButtonStyle, Interaction, Embed
import asyncio

from selenium import webdriver

from watchsama.cogs.mal.API.RawAnimeData import SeleniumRawData
from watchsama.cogs.mal.API.Embeds import BasicEmbed, ExtendedEmbed

class SearchView(View):
    
    def __init__(self, urls = [], url_index = 0 ,timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self._urls = urls
        self._url_index = url_index

    async def on_timeout(self) -> None:
        # Step 2
        children: list[Button] = self.children
        for item in children:
            item.disabled = True

        # Step 3
        await self.message.edit(view=self)


    @property
    def urls(self):
        return self._urls

    @property
    def url_index(self):
        return self._url_index
    
    @url_index.setter
    def url_index(self, url_index):
        self._url_index = url_index

class RightSearchButton(Button):

    def __init__(self, parent, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'right-button', url = None, emoji = '▶️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._parent = parent

    
    async def callback(self, interaction: Interaction):

        parent: SearchView = self._parent
        urls = parent.urls
        parent.url_index += 1

        if parent.url_index > len(urls) - 1:
            parent.url_index = 0


        await interaction.response.edit_message(content= f'Here are some entries that might fit your search: {parent.urls[parent.url_index]}')

class LeftSearchButton(Button):

    def __init__(self, parent, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'left-button', url = None, emoji = '◀️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._parent = parent


    async def callback(self, interaction: Interaction):
        
        parent: SearchView = self._parent
        urls = parent.urls
        parent.url_index -= 1
        if parent.url_index < 0:
            parent.url_index = len(urls) - 1
        
        await interaction.response.edit_message(content= f'Here are some entries that might fit your search: {parent.urls[parent.url_index]}')





class MALView(View):
    
    def __init__(self, embeds = [], embed_index = 0, data = [], data_index = 0, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self._embed_index = embed_index
        self._embeds = embeds
        self._data = data
        self._data_index = data_index

    async def on_timeout(self) -> None:
        # Step 2
        children: list[Button] = self.children
        for item in children:
            item.disabled = True

        # Step 3
        await self.message.edit(view=self)

    @property
    def embed_index(self):
        return self._embed_index
    
    @embed_index.setter
    def embed_index(self, index):
        self._embed_index = index

    @property
    def embeds(self):
        return self._embeds
    
    @embeds.setter
    def embeds(self, embeds):
        self._embeds = embeds

    @embeds.deleter
    def embeds(self):
        self._embeds = None
        self._embed_index = 0
    
    @property
    def data(self):
        return self._data

    @property
    def data_index(self):
        return self._data_index
    
    @data_index.setter
    def data_index(self, data_index):
        self._data_index = data_index


class RightButton(Button):

    def __init__(self, parent, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'right-button', url = None, emoji = '▶️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._parent = parent

    
    async def callback(self, interaction: Interaction):

        parent: MALView = self._parent
        embeds = parent.embeds
        parent.embed_index += 1

        if parent.embed_index > len(embeds) - 1:
            parent.embed_index = 0


        await interaction.response.edit_message(embed = embeds[parent.embed_index])
class LeftButton(Button):

    def __init__(self, parent, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'left-button', url = None, emoji = '◀️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._parent = parent


    async def callback(self, interaction: Interaction):
        
        parent: MALView = self._parent
        embeds = parent.embeds
        parent.embed_index -= 1
        if parent.embed_index < 0:
            parent.embed_index = len(embeds) - 1
        
        await interaction.response.edit_message(embed = embeds[parent.embed_index])

class LoadButton(Button):

    def __init__(self, parent, style = ButtonStyle.green, label = 'More', disabled = False, custom_id = 'load-button', url = None, emoji = None, row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._parent = parent

    def _embed_generator(self) -> list[BasicEmbed]:
        parent: MALView = self._parent
        driver = webdriver.Chrome()
        print(f'Driver: {driver} has been opened')
        parent.data_index += 1
        if parent.data_index > len(parent.data) - 1:
            parent.data_index = 0
        
        data = parent.data[parent.data_index]
    
        embeds = []
        for anime in data:
            url = anime['reference']
            title= anime['name']
            media =  anime['media']
            status = anime['status']
            image = anime['image']
            
            description = SeleniumRawData.get_Description(driver, url)
            embed = BasicEmbed(url = url, title = title, media = media, status = status, description = description, image=image)
            embeds.append(embed)
        

        driver.close()
        print(f'Driver: {driver} has been closed')

        return embeds
    

    async def callback(self, interaction: Interaction):
        parent: MALView = self._parent
        await interaction.response.defer(thinking=True)
       
        embeds = self._embed_generator()
        parent.stop()

        new_view = MALViewBuilder.create_View(embeds = embeds,data= parent.data, data_index = parent.data_index)
    
        await interaction.followup.send(content="Loaded more content", view=new_view, embed = embeds[0])


class WatchingLoadButton(LoadButton):

    def __init__(self, parent, style=ButtonStyle.green, label='More', disabled=False, custom_id='load-button', url=None, emoji=None, row=None):
        super().__init__(parent, style, label, disabled, custom_id, url, emoji, row)

    def _embed_generator(self) -> list[ExtendedEmbed]:
        parent: MALView = self._parent
        driver = webdriver.Chrome()
        print(f'Driver: {driver} has been opened')
        parent.data_index += 1
        if parent.data_index > len(parent.data) - 1:
            parent.data_index = 0
        
        data = parent.data[parent.data_index]
    
        embeds = []
        for anime in data:
            url = anime['reference']
            title= anime['name']
            media =  anime['media']
            status = anime['status']
            image = anime['image']
            progress = anime['progress']
            description = SeleniumRawData.get_Description(driver, url)
            embed = ExtendedEmbed(url = url, title = title, media = media, status = status, description = description, image=image, current=progress[0], end=progress[1])
            embeds.append(embed)
        

        driver.close()
        print(f'Driver: {driver} has been closed')

        return embeds
    
    async def callback(self, interaction: Interaction):
        parent: MALView = self._parent
        await interaction.response.defer(thinking=True)
       
        embeds = self._embed_generator()
        parent.stop()

        new_view = MALViewBuilder.create_Watching_View(embeds = embeds,data= parent.data, data_index = parent.data_index)
    
        await interaction.followup.send(content="Loaded more content", view=new_view, embed = embeds[0])


class MALViewBuilder():

    @staticmethod
    def create_View(embed_index = 0, embeds = [], data:list[list] = [], data_index = 0) -> MALView:
        view = MALView(embed_index = embed_index, embeds = embeds, data=data, data_index = data_index)
        right_button = RightButton(parent = view)
        load_button = LoadButton(parent =  view)
        left_button= LeftButton(parent = view)
        view.add_item(left_button)
        view.add_item(load_button)
        view.add_item(right_button)
        return view
    
    @staticmethod
    def create_Search_View(urls) -> SearchView:
        view = SearchView(urls = urls)
        right_button = RightSearchButton(parent = view)
        left_button = LeftSearchButton(parent = view)
        view.add_item(left_button)
        view.add_item(right_button)
        
        return view
    
    @staticmethod
    def create_Watching_View(embed_index = 0, embeds = [], data:list[list] = [], data_index = 0) -> MALView:
        view = MALView(embed_index = embed_index, embeds = embeds, data=data, data_index = data_index)
        right_button = RightButton(parent = view)
        load_button = WatchingLoadButton(parent = view)
        left_button= LeftButton(parent = view)
        view.add_item(left_button)
        view.add_item(load_button)
        view.add_item(right_button)
        return view