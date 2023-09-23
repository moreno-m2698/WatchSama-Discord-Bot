from discord.ui import View, Button
from discord import ButtonStyle

class RightButton(Button):

    def __init__(self, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'right-button', url = None, emoji = '▶️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
    

class LeftButton(Button):

    def __init__(self, style = ButtonStyle.primary, label = None, disabled = False, custom_id = 'left-button', url = None, emoji = '◀️', row = None):
        super().__init__(style=style, label=label, disabled=disabled,custom_id=custom_id,url=url,emoji=emoji,row=row)
    


class ViewBuilder():

    @staticmethod
    def create_View() -> View:
        view = View()
        right_button = RightButton()
        left_button= LeftButton()
        view.add_item(left_button)
        view.add_item(right_button)
        return view
    
    def _add_Children() -> None:
        pass