from discord.ui import View, Button
from discord import ButtonStyle

class RightButton(Button):

    def __init__(self, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'right-button', url = None, emoji = '▶️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
    

class LeftButton(Button):

    def __init__(self, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'left-button', url = None, emoji = '◀️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)

class MALView(View):
    
    def __init__(self, embed_index = 0, timeout: float | None = 180):
        super().__init__()
        self._embed_index = embed_index

    @property
    def embed_index(self):
        return self._embed_index

    @embed_index.setter
    def embed_index(self, embed_index):
        self._embed_index = embed_index

class MALViewBuilder():

    @staticmethod
    def create_View(embed_index = 0) -> MALView:
        view = MALView(embed_index = embed_index)
        right_button = RightButton()
        left_button= LeftButton()
        view.add_item(left_button)
        view.add_item(right_button)
        return view
    
    def _add_Children() -> None:
        pass