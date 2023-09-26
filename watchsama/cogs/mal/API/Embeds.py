from discord import Embed, Colour
from watchsama.tools import WatchSamaEmbed

class BasicEmbed(WatchSamaEmbed):
    
    ''' Base Embeds for MAL Cog'''

    def __init__(self, url: str , title: str, description, media, status, image):
        super().__init__(url = url, title = title, description = description)
        self._media = media
        self._status = status
        self.set_image(url = image)

    @property
    def media(self) -> str:
        return self._media
    
    @property
    def status(self) -> str:
        return self._status

