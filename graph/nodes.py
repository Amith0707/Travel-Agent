# Setting up dummy nodes for now
from .state import TravelState
from utils.logger import setup_logger
logger=setup_logger()
from modules.supervisor import decide_next_node # Supervisor Node
from modules.attractions import get_attractions #seper call to get attractions
from modules.weather import get_weather_forecast

def get_user_input(state:TravelState)->TravelState:
    try:
        '''Node to clean user input and format it into a nice query'''
        print("Entered node 1 in nodes.py..")
        logger.info("Entered node 1 in nodes.py..")

        user_input=state.get("user_input",{})

        query=f'''I live in {user_input.get("current_city")}
        and I want to Travel to {user_input.get("destination_city")} from
        {user_input.get("start_date")} to {user_input.get("end_date")}.

        I want to explore the popular places and try out the best restaurants in the city.

        Also suggest me some nice hotels to stay in where my hotel budget is:{user_input.get("hotel_budget")}. 

        Finally plan an entire itenerary for the entire duration of travel and make sure to keep the trip affordable within my Travel budget which is:{user_input.get("travel_budget")} and show me the estimated cost in the destination currency.'''

        #updating query key in TravelState
        print("\n Query is:",query)
        print("****************Exiting Node********************")
        state["query"]=query

        return state
    except Exception as e:
        print("ERROR in Node 1")
        logger.error(f"ERROR in Node 1: {e}")

def supervisor_route(state:TravelState)->TravelState:
    try:
        '''Calling the brain of our workflow'''
        print("Entered the supervisor Node in workflow")
        logger.info("Entered the supervisor Node in workflow")

        result=decide_next_node(state) # Updated state goes in here

        return result # This is a state as class is shared by all modules

    except Exception as e:
        print("ERROR in Node 2 Supervisor Node...")
        logger.error(f"ERROR in Node 2 Supervisor Node... :{e}")

def fetch_attractions(state:TravelState)->TravelState:
    """This node is called by supervisor to fetch Tourist spots in the destination city"""
    try:
        logger.info("Entered Fetch_attarctions node in node.py")
        #Fetching Destination
        destination=state.get("user_input",{}).get('destination_city')
        # Sending destination to the serper and updating state
        state['attractions']=get_attractions(destination) #Tourist spot input ?

        return state
    except Exception as e:
        logger.error("Error occured in fetch_attractions in node.py",e)

def fetch_weather_data(state:TravelState)->TravelState:
    '''
    This Node is used to fetch real time weather data...'''
    print("="*50)
    logger.info("ENtered weather node")
    try:
        # retrieving the dates
        destination=state.get("user_input").get("destination_city")
        from_date=state.get("user_input").get("start_date")
        end_date=state.get("user_input").get("end_date")
        #Calling the weather Modules
        weather_data=get_weather_forecast(destination,from_date,end_date)
        #updating the state
        state["weather"]=weather_data #need to fix the state or input
        logger.info("Weather Data updated Successfully in state...")

        return state
    except Exception as e:
        logger.error(f"Error in fetch_weather_data..{e}")

def filter_attractions(state: TravelState) -> TravelState:
    """
    Filters attractions based on simple weather rules.
    Example: if rain is likely, skip outdoor-heavy attractions.
    """
    print("=" * 50)
    logger.info("Entered filter_attractions node")

    try:
        attractions = state.get("attractions", [])
        weather_data = state.get("weather", {})

        if not attractions:
            logger.warning("No attractions found in state!")
            return state
        if not weather_data:
            logger.warning("No weather data found in state!")
            return state

        # Rule: if rain probability > 50% on any trip day, avoid outdoor/park attractions
        rainy = any(
            day.get("rain_prob", 0) > 50 or "rain" in day.get("condition", "").lower()
            for day in weather_data.values()
        )#--->this is correct 

        filtered = []
        for attr in attractions:
            title = attr.get("title", "").lower()
            category = attr.get("category", "").lower()

            if rainy and ("park" in title or "garden" in category or "outdoor" in category):
                # so basically if it's rainy that day and tourist spot is a park garden or any outdoor we skipppp
                logger.info(f"Skipping {attr.get('title')} due to rain forecast")
                continue

            filtered.append(attr)

        state["filtered_attractions"] = filtered
        logger.info(f"Filtered {len(filtered)} attractions (out of {len(attractions)})")
        return state

    except Exception as e:
        logger.error(f"Error in filter_attractions node: {e}")
        return state


def fetch_hotels(state):
    print("="*50)
    print("ENtered fetch hotels node")

def fetch_restaurants(state):
    print("="*50)
    print("Entered Fetch Restaurants node")

def generate_itinerary(state):
    print("="*50)
    print("Entered Generate Itinerary Node")

def currency_conversion(state):
    print("="*50)
    print("Entered Currency COnversion Node")

def calculate_expenses(state):
    print("="*50)
    print("Entered Currency Conversion Node")

def summarize(state):
    print("="*50)
    print("Entered Summarizer Node")