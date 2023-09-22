from discord import Embed, Colour

class BasicEmbed(Embed):
    
    def __init__(self, url: str , title: str, description, media, status):
        super().__init__(url = url, title = title, description = description)
        self._media = media
        self._status = status
