from discord.ui import View, Button
from discord import ButtonStyle, Interaction, Embed

from selenium import webdriver

class RightButton(Button):

    def __init__(self, embed_index, embeds, parent, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'right-button', url = None, emoji = '▶️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._embed_index = embed_index
        self._embeds = embeds

    @property
    def embed_index(self):
        
        return self._embed_index
    
    async def callback(self, interaction: Interaction):

        self._embed_index += 1
        if self._embed_index > len(self._embeds) - 1:
            self._embed_index = 0

        await interaction.response.edit_message(content="pressed right button", embed = self._embeds[self._embed_index])
        # Issues is that embed index is on children but we need to point to the adult
    

class LeftButton(Button):

    def __init__(self, embed_index, embeds, parent, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'left-button', url = None, emoji = '◀️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._embed_index = embed_index
        self._embeds = embeds

    @property
    def embed_index(self):
        
        return self._embed_index

    async def callback(self, interaction: Interaction):
        
        self._embed_index -= 1
        if self._embed_index < 0:
            self._embed_index = len(self._embeds) - 1

        await interaction.response.edit_message(content="pressed left button", embed = self._embeds[self._embed_index])

class LoadButton(Button):
    def __init__(self, embed_index, style = ButtonStyle.green, label = 'More', disabled = False, custom_id = 'load-button', url = None, emoji = None, row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._embed_index = embed_index

    @property
    def embed_index(self):
        
        return self._embed_index

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content="pressed More button")

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

    @property
    def embeds(self):
        return self._embeds
    
    @embeds.setter
    def embeds(self, embeds):
        self._embeds = embeds
    
    @property
    def data_index(self):
        return self._data_index
    
    @data_index.setter
    def data_index(self, data_index):
        self._data_index = data_index

    def embed_generator(self) -> list[Embed]:
        
        driver = webdriver.Chrome()

        driver.close()
        
        
        pass
    


class MALViewBuilder():

    @staticmethod
    def create_View(embed_index = 0, embeds = [], data:list[list] = []) -> MALView:
        view = MALView(embed_index = embed_index, embeds = embeds, data=data)
        right_button = RightButton(embed_index=0, embeds = embeds)
        load_button = LoadButton(embed_index=0)
        left_button= LeftButton(embed_index=0, embeds = embeds)
        view.add_item(left_button)
        view.add_item(load_button)
        view.add_item(right_button)
        return view
    