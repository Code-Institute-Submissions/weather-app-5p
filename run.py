import weather_wrapper
import os
import pycountry
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
if os.path.exists('env.py'):
    import env  # noqa

message = ""
data_message = ""
country_tuples = []

for i in pycountry.countries:
    country_tuples.append((i.name, i.alpha_2))


country_list = [y[0] for y in country_tuples]

def print_banner():
    print("☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ")
    print(" __          __        _   _   ")
    print(" \ \        / /       | | | |  ")
    print("  \ \  /\  / /__  __ _| |_| |__   ___ _ __   _ __  _   _ ")
    print("   \ \/  \/ / _ \/ _` | __| '_ \ / _ \ '__| | '_ \| | | |")
    print("    \  /\  /  __/ (_| | |_| | | |  __/ |    | |_) | |_| |")
    print("     \/  \/ \___|\__,_|\__|_| |_|\___|_|    | .__/ \__, |")
    print("                                            | |     __/ |")
    print("                                            |_|    |___/ \n")
    print("☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ")


def print_menu():
    print(message)
    print("1) Get Todays Weather")
    print("2) See the forecast for next 5 days")
    print("3) Number Three")
    print("4) Number Four")
    print(data_message)


def get_selection_country():
    country_completer = WordCompleter(country_list)
    while True:
        os.system("clear")
        print_banner()
        print("Note: Auto completer is case sensitive")
        text = prompt("> Enter a country: ", completer=country_completer)
        if text in country_list:
            return text
        print("Please select a country using the auto completer")


def get_todays_weather():
    country = get_selection_country()
    town = input("> Enter Town Name : ")
    print("> Press enter to continue!")
    data = weather.get_current_weather(country, town)
    
    sunrise = datetime.utcfromtimestamp(int(data['sys']['sunrise'])).strftime('%H:%M:%S')
    sunset = datetime.utcfromtimestamp(int(data['sys']['sunset'])).strftime('%H:%M:%S')

    return (
        f"\nAt a temperature of {data['main']['temp']}c with lows of {round(data['main']['temp_min'])}c and highs of {round(data['main']['temp_max'])}c\n"
        f"With {data['main']['humidity']}% humidity and {data['clouds']['all']}% cloud coverage\n"
        f"Sunrise at {sunrise} and Sunset at {sunset}"
        )


def get_forecast():
    country = get_selection_country()
    town = input("> Enter Town Name : ")
    print("> Press enter to continue!")
    data = weather.get_full_forecast(country, town)
    text = ""
    for forecast in data:
        text += f"{forecast['dt_txt']} {forecast['main']['temp']}\n"
    return text


weather = weather_wrapper.Weather(os.environ.get("API_KEY"))

while True:
    os.system("clear")
    print_banner()
    print_menu()    
    selection = input("> ")
    if not selection.isdigit():
        os.system("clear")
        message = "Please enter a number from the list below!"
        print_banner()
        print_menu()
        continue
    
    if int(selection) > 4:
        os.system("clear")
        message = "Please enter a number from the list below!"
        print_banner()
        print_menu()
        continue

    message = ""
    data_message = ""
    os.system("clear")
    print_banner()
    print_menu()
    selection = int(selection)

    if selection == 1:
        print(get_todays_weather())
        input("Press Enter to continue!")

    if selection == 2:
        print(get_forecast())
        input("Press Enter to continue!")

    if selection == 3:
        pass
    if selection == 4:
        pass
