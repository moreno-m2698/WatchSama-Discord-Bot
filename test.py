import json
import requests

from bs4 import BeautifulSoup, SoupStrainer

import watchsama.config

class MALBS4Wrapper():

    @staticmethod
    def get_anime_list_html(status: int):
        '''Gets html for anime based on status number'''

        username = watchsama.config.mal_user()
        url = f'https://myanimelist.net/animelist/{username}?status={status}'
        request = requests.get(url)


        soup = BeautifulSoup(request.text, 'html.parser')
        table_tag = soup.table
        tbody_contents = table_tag.find_all('tbody')
        # print(tbody_contents)
        only_table_tags = SoupStrainer("table") 
        print(BeautifulSoup(request.text, "html.parser", parse_only=only_table_tags).prettify())

        #There is an extra tbody tag that is in table somehow???
        

MALBS4Wrapper.get_anime_list_html(1)