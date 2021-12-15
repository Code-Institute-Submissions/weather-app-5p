""" Module for the weather api wrapper """
import requests


class Weather:
    """ Class for handling requests to the https://openweathermap.org/ api """

    base_url = "http://api.openweathermap.org/data/2.5/"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_json_response(self, url):
        response = requests.get(url + f'&APPID={self.api_key}')
        if response.status_code == 200:
            return response.json()

        print("Whoops, something went wrong " + str(response.status_code))
        print(url + f'&APPID={self.api_key}')
