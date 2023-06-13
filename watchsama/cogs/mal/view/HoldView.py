
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
        self.disabled=True
        v: HoldView = self.watching_view
        hold: str = '3'
        watching: int = 0
        m = MALSeleniumWrapper
        await interaction.response.edit_message(content="This is a test", view = v)
        driver: WebDriver = m.get_WebDriver()
        m.account_Login(driver=driver,username = mal_user(), password=mal_password())

        #Not sure if i should use this or go the followup webhook route

        m.get_MAL_Anime_List(username = mal_user(), driver=driver, status = hold)
        m.edit_Anime_Status(driver=driver, embed_index=v.embed_index, status = watching)
        v.embeds.pop(v.embed_index)

        await interaction.edit_original_response(content="Button located", view =v)

        #Button is located, implement press once we have finished task

        driver.close()
        print(v.embeds)

        #See about having a waiting embed while this is occuring




    #TODO: Plan out button removal process
