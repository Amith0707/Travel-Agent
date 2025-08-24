import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from graph.state import TravelState
from utils.logger import setup_logger
from utils.constants import OPENAI_MODEL,CURRENCY_DETECT_TEMPLATE
import json #--> to parse Json dict from LLM
import requests
load_dotenv()
logger = setup_logger()
API_KEY = os.getenv("OPENAI_API_KEY")
model=OPENAI_MODEL
currency_llm=ChatOpenAI(api_key=API_KEY,model=model)

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")  # from exchangerate-api
EXCHANGE_BASE_URL = "https://v6.exchangerate-api.com/v6"


def detect_currency(state:TravelState)->TravelState:
    try:
        logger.info("ENtered detect_currency module...")
        user_input=state.get("user_input")
        current_city=user_input.get("current_city","")
        destination_city=user_input.get("destination_city","")
        prompt=PromptTemplate(
            template=CURRENCY_DETECT_TEMPLATE,
            partial_variables={
                "current_city":current_city,
                "destination_city":destination_city
            }
        )
        chain=prompt|currency_llm
        response=chain.invoke({})
        logger.info(f"Currency Detection Ran Successfully..")
        try:
            currency_dict=json.loads(response.content)
        except Exception as e:
            print("Error in JSON Response while loading...",e)

        print("="*50)
        print("Currencies fetched..",currency_dict)
        print("="*50)

        #updating state
        state["from_currency"] = currency_dict.get("from_currency","")
        state["to_currency"] = currency_dict.get("to_currency","")

        # Hitting the currency exchange rate
        convert_currency(state["from_currency"],state["to_currency"],state)
        return state
    except Exception as e:
        logger.error(f"Error in detecting currency {e}")

def convert_currency(from_currency:str,to_currency:str,state:TravelState):
    """
    Uses from_currency and to_currency in state to fetch real-time exchange rate
    and updates state["exchange_value"].
    """
    try:
        logger.info("Entered convert_currency in currency.py to hit the api")
        url = f"{EXCHANGE_BASE_URL}/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}"
        response = requests.get(url)
        data = response.json()

        if data.get("result") == "success":
            rate = data.get("conversion_rate", 1.0)
            logger.info(f"Exchange rate fetched: {from_currency} -> {to_currency} = {rate}")
            state["exchange_value"] = rate
        else:
            logger.error(f"Failed to fetch exchange rate: {data}")
            state["exchange_value"] = 1.0
    except Exception as e:
        logger.error("Error in currency conversion...{e}")


