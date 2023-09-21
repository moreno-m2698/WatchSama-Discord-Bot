from typing import Any, Optional, Union
import discord
from discord.emoji import Emoji

from discord.enums import ButtonStyle
from discord.ext import commands
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import View, Button


class MALView(View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        
    def message_awareness(self, message) -> None:
        self.message = message
    
    def embeds_awareness(self, embeds: list[discord.Embed]) -> None:
        self.embeds = embeds

    def embed_index_awareness(self, index: int) -> None:
        self.embed_index = index

    def embed_range_awareness(self, range: list[int]) -> None:
        self.range = range



#TODO: work on these buttons
class LeftEmbedButton(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

    async def callback():
        pass

class RightEmbedButton(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

    async def callback():
        pass