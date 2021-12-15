import weather_wrapper
import os
from datetime import datetime

message = ""
data_message = ""


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
    print("2) Number Two")
    print("3) Number Three")
    print("4) Number Four")
    print(data_message)


weather = weather_wrapper.Weather("ff1832382941d09cdaaa8c1882e88ade")
print_banner()
print_menu()

while True:
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
        country = input("> Enter Country Name : ")
        town = input("> Enter Town Name : ")
        print("> Press enter to continue!")
        data = weather.get_current_weather(country, town)
        
        sunrise = datetime.utcfromtimestamp(int(data['sys']['sunrise'])).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(int(data['sys']['sunset'])).strftime('%H:%M:%S')

        data_message = (
            f"\nAt a temperature of {data['main']['temp']}c with lows of {round(data['main']['temp_min'])}c and highs of {round(data['main']['temp_max'])}c\n"
            f"With {data['main']['humidity']}% humidity and {data['clouds']['all']}% cloud coverage\n"
            f"Sunrise at {sunrise} and Sunset at {sunset}"
            )

    if selection == 2:
        pass
    if selection == 3:
        pass
    if selection == 4:
        pass
