# Simple task: 
# 1.Recieve Destination
# 2. Send Attractions via Updating TravelState
import requests
from typing import List,Dict
import os
from dotenv import load_dotenv
load_dotenv()
serper_api_key=os.getenv("SERPER_API_KEY")

from utils.logger import setup_logger
logger=setup_logger()

def get_attractions(destination:str,top_n:int =10)->List[Dict]: # default 10
    '''
    This Function fetches the tourist spots based on the destination city
    of the user and returns a list of Dictionary
    '''
    try:
        # Calling Langchain Serper tool
        from langchain_community.utilities import GoogleSerperAPIWrapper
        from langchain_core.tools import tool
        search=GoogleSerperAPIWrapper(type="places",serper_api_key=serper_api_key)
        logger.info("Searching for attractions using serper...")
        print("="*50)
        print(f"SEARCHING FOR TOURIST SPOTS IN {destination}")
        print("="*50)

        # Querying the serper search engine
        results=search.results(f"Top {top_n} tourist places in {destination}")
        places=results.get("places",[])

        # Extracting necessary info from json output
        attractions_list=[]
        for place in places[:top_n]:
            attraction={
                "title":place.get("title"),
                "address":place.get("address"),
                "rating":place.get("rating"),
                "website":place.get("website"),
                "phoneNumber":place.get("phoneNumber"),
                "category":place.get("category")
            }
            print("="*50)
            print(attraction)
            print("="*50)
            attractions_list.append(attraction)

        logger.info(f"Fetched {len(attractions_list)} attractions for {destination} successfully")
        print(attractions_list) #bas dekhna haii-->
        return attractions_list


    except Exception as e:
        logger.error(f"Error in get_attractions while fetching attractions in attractions.py for {destination}: {e}")
        return []


