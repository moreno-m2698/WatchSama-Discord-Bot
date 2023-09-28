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
        self._emoji_bar_dict = {
            'e1': "<:Empty_Bar_1:1115750121913733232>",
            'e2': "<:Empty_Bar_2:1115750137747210240>",
            'f1': "<:Filled_Bar_1:1115750151194165269>",
            'f2': "<:Filled_Bar_2:1115750166364954655>",
            'h1': "<:Heart_Bar_1:1115750030956044338>",
            'h2': "<:Heart_Bar_2:1115750086761250876>",
            'h3': "<:Heart_Bar_3:1115750104041803916>"
        }


    @property
    def current(self) -> str:
        return self._current
    
    @property
    def end(self) -> str:
        return self._end
    
    @property
    def progress(self):
        return f"{self.current} / {self.end}"
    
    @property
    def progress(bar):
        pass