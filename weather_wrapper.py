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
        """ note that with free api cannot go further back than 5days """

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

    def get_single_forecast(self, country, town, date):
        """ note that without subscription cannot go further than 5days """

        # given date in unix time
        param_date = datetime.strptime(date, "%d/%m/%Y")
        # today in unix time
        today_timestamp = int(datetime.timestamp(datetime.now()))
        # 5 day cutoff for free api use, 432000 = 5days in seconds
        cutoff_timestamp = today_timestamp + 432000

        if int(param_date.timestamp()) not in range(today_timestamp, cutoff_timestamp):
            print("Date surpasses 5 day limit")
            return

        request_url = (
            self.base_url +
            'forecast'
            f'?q={town},{country}&mode=json'
            '&units=metric'
        )
        values = self.get_json_response(request_url)
        return_values = []
        date_format = "%Y-%m-%d %H:%M:%S"

        for i in values["list"]:
            if (datetime.strptime(i["dt_txt"], date_format).timetuple().tm_mday
                    == param_date.timetuple().tm_mday):
                return_values.append(i)

        return return_values

# from weather_wrapper import *
# x = Weather("488f542cdab9f254e7b00827c439d379")
# y = x.get_single_forecast("united kingdom","crawley","16/12/2021")