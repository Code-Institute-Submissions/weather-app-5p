""" Module for the weather api wrapper """
import requests
from datetime import datetime
import time


class Weather:
    """ Class for handling requests to the https://openweathermap.org/ api """

    BASE_URL = "http://api.openweathermap.org/data/2.5/"

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
            self.BASE_URL +
            'weather' +
            f'?q={town},{country}'
            '&units=metric'
        )
        return self.get_json_response(request_url)

    def get_historical_weather(self, country, town, date):
        """ note that with free api cannot go further back than 5days """
        timetuple = datetime.strptime(date, "%Y-%m-%d").timetuple()
        timestamp = int(time.mktime(timetuple))

        if (datetime.now().day - timetuple.tm_mday) not in range(0, 6):
            print("Date surpasses 5 day limit")
            return

        current_weather = self.get_current_weather(country, town)
        
        request_url = (
            self.BASE_URL +
            'onecall/timemachine'
            f'?lat={str(current_weather["coord"]["lat"])}'
            f'&lon={str(current_weather["coord"]["lon"])}'
            f'&dt={int(timestamp)}'
            '&units=metric'
        )

        return self.get_json_response(request_url)

    def get_full_forecast(self, country, town):
        """ 
        Gets a 5day forecast from time queried,
        does not include data from earlier in the day 
        https://openweathermap.org/forecast5 
        """

        request_url = (
            self.BASE_URL +
            'forecast'
            f'?q={town},{country}&mode=json'
            '&units=metric'
        )
        return self.get_json_response(request_url)["list"]

    def get_single_forecast(self, country, town, date):
        """ note that without subscription cannot go further than 5days """
        values = self.get_full_forecast(country, town)

        # given date in unix time
        param_date = datetime.strptime(date, "%d/%m/%Y")

        return_values = []
        date_format = "%Y-%m-%d %H:%M:%S"

        for i in values:
            if (datetime.strptime(i["dt_txt"], date_format).timetuple().tm_mday
                    == param_date.timetuple().tm_mday):
                return_values.append(i)

        return return_values
