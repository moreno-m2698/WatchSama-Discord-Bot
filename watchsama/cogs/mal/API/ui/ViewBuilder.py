from discord.ui import View, Button
from discord import ButtonStyle, Interaction, Embed

from selenium import webdriver

class RightButton(Button):

    def __init__(self, embed_index, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'right-button', url = None, emoji = '▶️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._embed_index = embed_index

    @property
    def embed_index(self, interaction: Interaction):
        
        return self._embed_index
    
    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content="pressed right button")
    

class LeftButton(Button):

    def __init__(self, embed_index, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'left-button', url = None, emoji = '◀️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
        self._embed_index = embed_index

    @property
    def embed_index(self, interaction: Interaction):
        
        return self._embed_index

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content="pressed left button")

class MALView(View):
    
    def __init__(self, embeds = [], embed_index = 0, data = [], timeout: float | None = 180):
        super().__init__()

        self._embeds = embeds
        self._data = data
        self._data_index = 0



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

        ''' We will use this to create embeds once we need more'''
        pass
    


class MALViewBuilder():

    @staticmethod
    def create_View(embed_index = 0, embeds = [], data:list[list] = []) -> MALView:
        view = MALView(embed_index = embed_index, embeds = embeds, data=data)
        right_button = RightButton(embed_index=0)
        left_button= LeftButton(embed_index=0)
        view.add_item(left_button)
        view.add_item(right_button)
        return view
    