
from typing import Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.partial_emoji import PartialEmoji
from discord.ui import Button
from selenium.webdriver.remote.webdriver import WebDriver


from .MALView import MALView
from watchsama.cogs.mal.API.MALSelenium import MALSeleniumWrapper, cache_anime_meta
from watchsama.config import App_Config

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
        hold_status: str = '3'
        watching_status: str = '1'
        watching_select_index: int = 0
        m = MALSeleniumWrapper
        
        await interaction.response.edit_message(content="This is a test", view = v)
        driver: WebDriver = m.get_WebDriver(isTesting=True)
        m.account_Login(driver=driver,username = App_Config.mal_user(), password=App_Config.mal_password())

        #Not sure if i should use this or go the followup webhook route

        m.get_MAL_Anime_List(username = App_Config.mal_user(), driver=driver, status = hold_status)
        m.edit_Anime_Status(driver=driver, embed_index=v.embed_index, status = watching_select_index)
        v.embeds.pop(v.embed_index)
        cache_anime_meta(hold_status)
        cache_anime_meta(watching_status)
        print('ran cache')


        await interaction.edit_original_response(content="Button located", view =v)

        #Button is located, implement press once we have finished task

        driver.close()


        #See about having a waiting embed while this is occuring




    #TODO: Plan out button removal process
