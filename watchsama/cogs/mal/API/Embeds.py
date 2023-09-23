from discord import Embed, Colour

class BasicEmbed(Embed):
    
    ''' Base Embeds for MAL Cog'''

    def __init__(self, url: str , title: str, description, media, status, image):
        super().__init__(url = url, title = title, description = description, color=Colour.from_str('#FFB7C5'))
        self._media = media
        self._status = status
        self.set_image(url = image)
        self.set_author(name = 'Watch-Sama')

    @property
    def media(self) -> str:
        return self._media
    
    @property
    def status(self) -> str:
        return self._status