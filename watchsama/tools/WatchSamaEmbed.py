from discord import Embed, Colour

class WatchSamaEmbed(Embed):

    ''' Base Embeds for WatchSama'''

    def __init__(self, colour = Colour.from_str('#FFB7C5'), title = None, type = 'rich', url = None, description = None, timestamp =  None):
        super().__init__(color=Colour.from_str('#FFB7C5'), title = None, type = 'rich', url = None, description = None, timestamp =  None)
        self.set_author(name = 'Watch-Sama')