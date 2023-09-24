from discord.ui import View, Button
from discord import ButtonStyle, Interaction, Embed

from selenium import webdriver

from watchsama.cogs.mal.API.RawAnimeData import SeleniumRawData
from watchsama.cogs.mal.API.Embeds import BasicEmbed

class MALView(View):
    
    def __init__(self, embeds = [], embed_index = 0, data = [], timeout: float | None = 180):
        super().__init__()
        self._embed_index = embed_index
        self._embeds = embeds
        self._data = data
        self._data_index = 0

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


        await interaction.response.edit_message(content="pressed right button", embed = embeds[parent.embed_index])
        # Issues is that embed index is on children but we need to point to the adult
    

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
        
        await interaction.response.edit_message(content="pressed left button", embed = embeds[parent.embed_index])

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
        del parent.embeds
        new_embeds = self._embed_generator()
        parent.embeds = new_embeds
        embeds = parent.embeds

        #Discord interaction is not working for some reason?
        # Hypothesize that it may hve to do with changing the embeds entirely
        # Might need to remake a new view each time

        await interaction.response.edit_message(content="pressed More button", embed = embeds[parent.embed_index])


class MALViewBuilder():

    @staticmethod
    def create_View(embed_index = 0, embeds = [], data:list[list] = []) -> MALView:
        view = MALView(embed_index = embed_index, embeds = embeds, data=data)
        right_button = RightButton(parent = view)
        load_button = LoadButton(parent =  view)
        left_button= LeftButton(parent = view)
        view.add_item(left_button)
        view.add_item(load_button)
        view.add_item(right_button)
        return view
    