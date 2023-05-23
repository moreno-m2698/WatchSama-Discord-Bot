import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
from discord.ui import View, Button

class WatchingView(View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        reroll_button=ReRollButton(style=discord.ButtonStyle.green, label="switch", watching_view=self)
        url_button = Button(label = 'Anime List', url = "https://myanimelist.net/animelist/gabslittlepogger")
        self.add_item(reroll_button)
        self.add_item(url_button)
        
    def message_awareness(self, message) -> None:
        self.message = message
    
    def embeds_awareness(self, embeds: list[discord.Embed]) -> None:
        self.embeds = embeds

    def embed_index_awareness(self, index: int) -> None:
        self.embed_index = index

class ReRollButton(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, watching_view: WatchingView):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.watching_view = watching_view
        
    
    async def callback(self, interaction: discord.Interaction):
        if self.watching_view.embed_index == 0:
            self.watching_view.embed_index = 1
            
            
        elif self.watching_view.embed_index == 1:
            self.watching_view.embed_index = 0
        
        await interaction.response.edit_message(content="embed swap",embed = self.watching_view.embeds[self.watching_view.embed_index], view=self.watching_view)
        