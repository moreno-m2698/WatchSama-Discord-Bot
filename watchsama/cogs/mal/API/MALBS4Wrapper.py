import json
import requests

from bs4 import BeautifulSoup

from ....config import mal_user

class MALBS4Wrapper():

    @staticmethod
    def get_anime_list_html(status: int):
        '''Gets html for anime based on status number'''

        username = mal_user()
        url = f'myanimelist.net/animelist/{username}?status={status}'
        request = requests.get(url)


        soup = BeautifulSoup(request.text, 'html.parser')
        print(soup.prettify())

MALBS4Wrapper.get_anime_list_html(1)