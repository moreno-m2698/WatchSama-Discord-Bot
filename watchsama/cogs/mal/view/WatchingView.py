import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
from discord.ui import View, Button
import random

from view.MALView import MALView
class WatchingView(MALView):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        reroll_button=ReRollButton(style=discord.ButtonStyle.green, label="switch", watching_view=self)
        url_button = Button(label = 'Anime List', url = "https://myanimelist.net/animelist/gabslittlepogger")
        self.add_item(reroll_button)
        self.add_item(url_button)
        

class ReRollButton(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, watching_view: WatchingView):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.watching_view = watching_view
        
    
    async def callback(self, interaction: discord.Interaction):
        new_index: int = random.randint(self.watching_view.range[0], self.watching_view.range[1])
        self.watching_view.embed_index = new_index
        # self.disabled = True
        await interaction.response.edit_message(content="embed swap",embed = self.watching_view.embeds[self.watching_view.embed_index], view=self.watching_view)
        