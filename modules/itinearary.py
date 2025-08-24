import os
from dotenv import load_dotenv
load_dotenv()
from utils.logger import setup_logger
logger=setup_logger()

from utils.constants import ITNERARY_TEMPLATE,OPENAI_MODEL

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from graph.state import TravelState
from typing import List, Dict

try:      
    api_key=os.getenv("OPENAI_API_KEY")
    model=OPENAI_MODEL
    llm=ChatOpenAI(api_key=api_key,model=model,temperature=0)
    print("LLM Initalized Successfully")
    logger.info("LLM Initalized Successfully")

except Exception as e:
    print("Error occured in Itnerary.py")
    logger.error("Error occured in Itnerary.py",e)

def create_itinerary(state: TravelState) -> List[str]: #itinerary:List[str]
    """
    Generate a day-wise itinerary using LLM based on current TravelState.
    
    Args:
        state (Dict): TravelState dictionary containing user_input, attractions, hotels, weather, etc.
        model_name (str): LLM model to use.
        temperature (float): Creativity level for generation.

    Returns:
        List[str]: Day-wise itinerary.
    """
    logger.info("Entered generate_interary..")
    user_input = state.get("query","")
    attractions = state.get("filtered_attractions", [])
    hotels = state.get("hotels",[])
    restaurants = state.get("restaurants",[])
    weather = state.get("weather",{})
    # Setting up the prompt
    prompt = PromptTemplate(
        template=ITNERARY_TEMPLATE,
        partial_variables={
            "user_input":user_input,
            "attractions":attractions,
            "hotels":hotels,
            "restaurants":restaurants,
            "weather":weather} #--->working here
    )
    chain=prompt|llm
    response=chain.invoke({})
    print("="*50)
    print("RESPONSE: \n",response.content)
    # extracting text from the response
    response_text = response.content if hasattr(response, "content") else str(response)
    # Split by line to get list of itinerary steps
    itinerary = [line.strip() for line in response_text.split("\n") if line.strip()]
    print("="*50)
    print("="*50)
    print("Printing Interaray")
    print(itinerary)
    print('~'*50)
    return itinerary