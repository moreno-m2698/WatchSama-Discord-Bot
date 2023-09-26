from watchsama.tools import WatchSamaEmbed

class BasicEmbed(WatchSamaEmbed):
    
    ''' Base Embeds for MAL Cog'''

    def __init__(self, url: str , title: str, description, media, status, image):
        super().__init__(url = url, title = title, description = description)
        self.set_image(url = image)
        self.add_field(name="Type:", value=media,inline=True)
        self.add_field(name="Watch status:", value=status, inline=True)    

class ExtendedEmbed(WatchSamaEmbed):

    def __init__(self, url: str , title: str, description, media, status, image, current, end):
        super().__init__(url = url, title = title, description = None, media = media, status= status)
        self._current = current
        self._end = end
        self.set_image(url = image)
        self.add_field(name= "Progress")
        self.add_field(name = "Description", value = description, inline=False)
        self.add_field(name="Type:", value=media,inline=True)
        self.add_field(name="Watch status:", value=status, inline=True)    


    @property
    def current(self) -> str:
        return self._current
    
    @property
    def end(self) -> str:
        return self._end
    
    @property
    def progress(self):
        return f"{self.current} / {self.end}"