
from typing import Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.partial_emoji import PartialEmoji
from discord.ui import Button
from selenium.webdriver.remote.webdriver import WebDriver

from .MALView import MALView
from watchsama.cogs.mal.API.MALSelenium import MALSeleniumWrapper
from watchsama.config import mal_user, mal_password

class HoldView(MALView):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        unhold_button = UnholdButton(label = "Unhold", style = discord.ButtonStyle.green, watching_view=self)
        self.add_item(unhold_button)


class UnholdButton(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, watching_view: HoldView):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.watching_view = watching_view
          
    async def callback(self, interaction: discord.Interaction):
        v: HoldView = self.watching_view
        self.disabled=True
        await interaction.response.edit_message(content="This is a test", view = v)
        driver: WebDriver = MALSeleniumWrapper.get_WebDriver()
        MALSeleniumWrapper.account_Login(driver=driver,username = mal_user(), password=mal_password())

        #Not sure if i should use this or go the followup webhook route

        MALSeleniumWrapper.get_MAL_Anime_List(username = mal_user(), driver=driver, status = '3')
        await interaction.edit_original_response(content="Successful connect", view = v)
        
        driver.close()

        #See about having a waiting embed while this is occuring




    #TODO: Plan out button removal process
