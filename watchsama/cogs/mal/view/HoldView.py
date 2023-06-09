from typing import Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
from discord.types.components import ButtonComponent as ButtonComponentPayload
from discord.ui import View, Button
import random

from .MALView import MALView

class HoldView(MALView):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)


class UnholdButton(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

    async def callback():
        pass


    #TODO: Plan out button removal process
