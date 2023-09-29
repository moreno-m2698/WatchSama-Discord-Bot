from watchsama.tools import WatchSamaEmbed
class BasicEmbed(WatchSamaEmbed):
    
    ''' Base Embeds for MAL Cog'''

    def __init__(self, url: str , title: str, description, media, status, image):
        if len(description) > 4096:
            description = description[0:4093] + '...'
        super().__init__(url = url, title = title, description = description)
        self.set_image(url = image)
        self.add_field(name="Type:", value=media,inline=True)
        self.add_field(name="Watch status:", value=status, inline=True)    

class ExtendedEmbed(WatchSamaEmbed):

    def __init__(self, url: str , title: str, description, media, status, image, current, end):
        super().__init__(url = url, title = title, description = None)
        self._current = current
        self._end = end
        self.set_image(url = image)
        self._emoji_bar_dict = {
            'e1': "<:e1:1157125885619621948>",
            'e2': "<:e2:1157125946407649330>",
            'f1': "<:f1:1157126002166747177>",
            'f2': "<:f2:1157126019950575627>",
            'h1': "<:e1:1157125768577548388>",
            'h2': "<:e2:1157125816682033202>",
            'h3': "<:e3:1157125868859166730>"
        }
        self.add_field(name= "Progress", value = self.progress_bar)
        if len(description) > 1024:
            description=description[0:1021] + '...'
        self.add_field(name = "Description", value = description, inline=False)
        self.add_field(name="Type:", value=media, inline=True)
        self.add_field(name="Watch status:", value=status, inline=True)  
        


    @property
    def current(self) -> str:
        return self._current
    
    @property
    def end(self) -> str:
        return self._end
    
    @property
    def progress_bar(self) -> str:
        
        ratio = self._current/self._end
        em = self._emoji_bar_dict
        if ratio == 1:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['h3'] + f"  {self._current} / {self._end}"
        if ratio >= .9:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['h2'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .8:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['h2'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .7:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['h2'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .6:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['h2'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .5:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['f2'] + em['h2'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .4:
            return em['f1'] + em['f2'] + em['f2'] + em['f2'] + em['h2'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .3:
            return em['f1'] + em['f2'] + em['f2'] + em['h2'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .2:
            return em['f1'] + em['f2'] + em['h2'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        if ratio >= .1:
            return em['f1'] + em['h2'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"
        else:
            return em['h1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e1'] + em['e2'] + f"  {self._current} / {self._end}"