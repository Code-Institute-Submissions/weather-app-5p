import os
from datetime import datetime, timedelta
import pycountry
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import weather_wrapper
if os.path.exists('env.py'):
    import env  # noqa

# Codes for changing text colors
red_text = '\033[91m'
yellow_text = '\033[93m'
white_text = '\033[0m'

message = ""
country_tuples = []

# Populate tuple list witg country name and iso 2 code
for i in pycountry.countries:
    country_tuples.append((i.name, i.alpha_2))

# create a list of only the country names
country_list = [y[0] for y in country_tuples]


def print_banner():
    """
    Displays the banner
    """
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
    """
    Displays the menu
    """
    print(message)
    print("1) Get Todays Weather")
    print("2) See the forecast for next 5 days")
    print("3) Get last 5 days weather")


def get_selection_country():
    """
    Gets user input for selecting a users country assisted by
    a word completer filled with all countries
    """
    # Create a WordCompleter object
    country_completer = WordCompleter(country_list)

    os.system("clear")

    print_banner()
    print(f"{yellow_text}Note: Auto completer is case sensitive{white_text}")

    # Loop until a valid country has been entered
    while True:
        # prompt acts like input() but has a completer when
        # given a list of values
        text = prompt("> Enter a country: ", completer=country_completer)

        # If a valid country has been
        if text in country_list:
            return text
        os.system("clear")
        print_banner()
        print(f"{yellow_text}Note: Auto completer "
              f"is case sensitive{white_text}")
        print(f"{red_text}Please select a country "
              f"using the auto completer{white_text}")


def get_selection_town():
    return input("> Enter Town Name : ")


def get_todays_weather():
    """
    Gets and builds a string of data to display the current days weather
    """
    country = get_selection_country()
    town = get_selection_town()

    # Get the iso alpha-2 code for the country
    country = [h for h in country_tuples if h[0] == country][0][1]
    current_weather = weather.get_current_weather(country, town)

    if isinstance(current_weather, str):
        return current_weather

    # Parse sunrise sunset from timestamp to a readable date
    sunrise = datetime.utcfromtimestamp(
        int(current_weather['sys']['sunrise'])).strftime('%H:%M:%S')
    sunset = datetime.utcfromtimestamp(
        int(current_weather['sys']['sunset'])).strftime('%H:%M:%S')

    return (
        f"\nAt a temperature of {current_weather['main']['temp']}c "
        f"with lows of {round(current_weather['main']['temp_min'])}c "
        f"and highs of {round(current_weather['main']['temp_max'])}c\n"
        f"A {current_weather['main']['humidity']}% humidity and "
        f"{current_weather['clouds']['all']}% cloud coverage\n"
        f"Sunrise at {sunrise} and Sunset at {sunset}"
    )


def get_forecast():
    """
    Get forecast for the next 5 days start from current day
    """
    country = get_selection_country()
    town = get_selection_town()

    # Get the iso alpha-2 code for the country
    country = [h for h in country_tuples if h[0] == country][0][1]
    full_forecast = weather.get_full_forecast(country, town)

    if isinstance(full_forecast, str):
        return full_forecast

    # temp - humidity - wind speed
    current_data = [0, 0, 0]
    current_date = ""
    loops = 0
    text = ""

    # Loop through each 3hour forecast and compile them into days
    for forecast in full_forecast["list"]:
        # Parse and change date into a  Y-m-d format
        str_date = str(datetime.strptime(
            forecast["dt_txt"], "%Y-%m-%d %H:%M:%S").date())

        # If date of forecast is different then append data and clear variables
        if str_date != current_date:
            if current_date != "":
                text += (f"{current_date} - "
                         f"{round(current_data[0]/loops, 2)}c - "
                         f"Humidity {round(current_data[1]/loops,2)}% - "
                         f"Windspeed {round(current_data[2]/loops, 2)}mps\n")
            current_data = [0, 0, 0]
            loops = 0
            current_date = str_date

        current_data[0] += forecast["main"]["temp"]
        current_data[1] += forecast["main"]["humidity"]
        current_data[2] += forecast["wind"]["speed"]

        # Count loops for when we average
        loops += 1

    # Append the final data
    text += (f"{current_date} - {round(current_data[0]/loops, 2)}c - "
             f"Humidity {round(current_data[1]/loops,2)}% - "
             f"Windspeed {round(current_data[2]/loops, 2)}mps\n")
    return text


def get_previous_weather():
    """
    Gets weather from past 5 days, due to using the free tier
    of api can only go as far back as 5 days
    """
    country = get_selection_country()
    town = get_selection_town()

    # Get the iso alpha-2 code for the country
    country = [h for h in country_tuples if h[0] == country][0][1]

    start_date = datetime.now().date()

    return_data = []

    # Loop for each of 5days from today
    for i in range(0, 6):
        date = start_date - timedelta(days=i)
        api_data = weather.get_historical_weather(country, town, str(date))

        if isinstance(api_data, str):
            return api_data

        # date - temp - humidity - wind speed
        avg = ["", 0, 0, 0]
        count = 0
        for item in api_data["hourly"]:
            count += 1
            avg[1] += item["temp"]
            avg[2] += item["humidity"]
            avg[3] += item["wind_speed"]

        avg[0] = date

        # Get averages and round
        avg[1] = round(avg[1] / count, 2)
        avg[2] = round(avg[2] / count, 2)
        avg[3] = round(avg[3] / count, 2)
        return_data.append(avg)

    print(f"{yellow_text}Note: Values are averages.{white_text}")
    text = ""
    for data in return_data:
        text += (
            f"{str(data[0])} - Temperature @ {data[1]}c - "
            f"Humidity @ {data[2]} - "
            f"Windspeed @ {data[3]}mps\n")

    return text


weather = weather_wrapper.Weather(os.environ.get("API_KEY"))

while True:
    # Clear the console
    os.system("clear")
    print_banner()
    print_menu()
    selection = input("> ")

    # Check if something other than a number is entered
    if not selection.isdigit():
        os.system("clear")
        message = (f"{red_text}Please enter a number "
                   f"from the list below!{white_text}")
        print_banner()
        print_menu()
        continue

    # Check if selection is greater than 3
    if int(selection) > 3:
        os.system("clear")
        message = (f"{red_text}Please enter a number "
                   f"from the list below!{white_text}")
        print_banner()
        print_menu()
        continue

    message = ""
    # Clear console and reprint screen with asked for data
    os.system("clear")
    print_banner()
    print_menu()
    selection = int(selection)

    if selection == 1:
        print(get_todays_weather())

    if selection == 2:
        print(get_forecast())

    if selection == 3:
        print(get_previous_weather())

    if selection == 4:
        pass

    input("Press Enter to continue!")
