
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands

from discord.ui import Button
import random

from .MALView import MALView

class HoldView(MALView):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)


class UnholdButton(discord.ui.Button):
    def __init__(self):
        super().__init__()

    async def callback():
        pass


    #TODO: Plan out button removal process
