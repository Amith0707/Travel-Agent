from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import List, Dict
import os
from utils.logger import setup_logger
logger=setup_logger()
# You should set this in your environment or pass it securely
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_hotels(destination_city: str, budget: float, check_in: str = None, check_out: str = None) -> List[Dict]:
    """
    Calls Serper Places API via LangChain wrapper to fetch hotels.
    
    Args:
        destination_city (str): City to search hotels in.
        budget (float): Budget per night in local currency.
        check_in (str): Optional check-in date (YYYY-MM-DD).
        check_out (str): Optional check-out date (YYYY-MM-DD).

    Returns:
        List[Dict]: List of hotels with relevant details.
    """
    logger.info("Entered search_hotels in hotels.py")
    search = GoogleSerperAPIWrapper(type="places", serper_api_key=SERPER_API_KEY)
    query = f"Suggest me 5 hotels in {destination_city} with a budget of {budget} rupees per night"
    if check_in and check_out:
        query += f" from {check_in} to {check_out}"

    results = search.results(query)
    
    hotels_list = []
    for hotel in results.get("places", []):
        hotels_list.append({
            "name": hotel.get("title"),
            "address": hotel.get("address"),
            "category": hotel.get("category"),
            "rating": hotel.get("rating"),
            "rating_count": hotel.get("ratingCount"),
            "phone": hotel.get("phoneNumber"),
            "website": hotel.get("website"),
        })
    
    return hotels_list
