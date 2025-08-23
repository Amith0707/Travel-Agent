# Fetch weather details
import os
from dotenv import load_dotenv
load_dotenv()
#Fetching Weather api key
weather_api_key=os.getenv("WEATHER_API_KEY")
from utils.logger import setup_logger

logger=setup_logger()

import requests
from datetime import datetime,timedelta

def get_weather_forecast(destination:str,start_date:str,end_date:str)->dict:
    """
    Fetches weather forecast for a given city between start_date and end_date.
    Returns a cleaned dict keyed by date with relevant info.
    """

    logger.info("Entered get_weather_forecast in nodes.py")
    logger.info(f"Fetching Weather Forecast Details on {destination} from {start_date} to {end_date}")
    #Calculating the time difference
    start_dt=datetime.strptime(start_date,"%Y-%m-%d")
    end_dt=datetime.strptime(end_date,"%Y-%m-%d")
    delta_days=(end_dt-start_dt).days+1 # +1 to include end_date

    # Capping forecast days till 7 Coz using free tier
    forecast_days=min(delta_days,7)

    #Calling weather api
    logger.info("Calling Weather API...")

    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={destination}&days={forecast_days}&aqi=no&alerts=no"
        resp=requests.get(url)
        data=resp.json()

        #Cleanning and filtering the data
        filtered_weather={}
        for day in data["forecast"]["forecastday"]:
            date_dt = datetime.strptime(day["date"], "%Y-%m-%d")
            if start_dt <= date_dt <= end_dt:
                filtered_weather[day["date"]] = { #-->based on dates keys are made which consist of below data in key-value ka pair
                    "avg_temp": day["day"]["avgtemp_c"],
                    "max_temp": day["day"]["maxtemp_c"],
                    "min_temp": day["day"]["mintemp_c"],
                    "condition": day["day"]["condition"]["text"],
                    "rain_prob": day["day"]["daily_chance_of_rain"],
                    "snow_prob": day["day"]["daily_chance_of_snow"]
                }
        logger.info("Filtered Weather Data Successfully..")
        return filtered_weather
    except Exception as e:
        logger.error(f"Error in get_weather_forecast data",e)