""" Module for the weather api wrapper """


class Weather:
    """ Class for handling requests to the https://openweathermap.org/ api """
    def __init__(self, api_key):
        self.api_key = api_key


