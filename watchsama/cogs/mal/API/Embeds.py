from discord import Embed, Colour

class BasicEmbed(Embed):
    
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