""" Module for the weather api wrapper """
import requests
from datetime import datetime, timedelta
import time

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

    def get_current_weather(self, country, town):
        request_url = (
            self.base_url +
            'weather' +
            f'?q={town},{country}'
        )
        return self.get_json_response(request_url)

    def get_historical_weather(self, country, town, date):
        """ note that without subscription cannot go futher back than 5days """
        timetuple = datetime.strptime(date, "%d/%m/%Y").timetuple()
        timestamp = time.mktime(timetuple)

        date_limit = datetime.now() - timedelta(days=6)
        if (datetime.now() - date_limit).days >= 6:
            print("Date surpasses 5 day limit")
            return

        current_weather = self.get_current_weather(country, town)

        request_url = (
            self.base_url +
            'onecall/timemachine'
            f'?lat={current_weather["coord"]["lat"]}'
            f'&lon={current_weather["coord"]["lon"]}'
            f'&dt={int(timestamp)}'
            '&units=matric'
        )

        return self.get_json_response(request_url)
