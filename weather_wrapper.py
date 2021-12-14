import requests
""" Module for the weather api wrapper """


class Weather:
    """ Class for handling requests to the https://openweathermap.org/ api """
    def __init__(self, api_key):
        self.api_key = api_key

    def json_respones(self, url):
        response = requests.get(url)
        if(response.status_code == requests.codes.ok):
            return response.json()
            
        print("Whoops, something went wrong")

    def get_current_weather(self):
        pass


