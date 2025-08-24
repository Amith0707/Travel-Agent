from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import List, Dict
import os
from utils.logger import setup_logger
logger=setup_logger()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_restaurants(destination_city: str, cuisine: str = None) -> List[Dict]:
    """
    Calls Serper Places API to fetch popular restaurants.
    
    Args:
        destination_city (str): City to search restaurants in.
        cuisine (str, optional): Filter by cuisine type.

    Returns:
        List[Dict]: List of restaurants with relevant details.
    """
    search = GoogleSerperAPIWrapper(type="places", serper_api_key=SERPER_API_KEY)
    query = f"Suggest me 5 popular local restaurants in {destination_city} which are famous with popular dish"
    if cuisine:
        query += f" serving {cuisine}"
    
    results = search.results(query)

    restaurants_list = []
    for restaurant in results.get("places", []):
        restaurants_list.append({
            "name": restaurant.get("title"),
            "address": restaurant.get("address"),
            "category": restaurant.get("category"),
            "rating": restaurant.get("rating"),
            "rating_count": restaurant.get("ratingCount"),
            "phone": restaurant.get("phoneNumber"),
            "website": restaurant.get("website"),
            "price_level": restaurant.get("priceLevel"),
        })
    
    return restaurants_list
