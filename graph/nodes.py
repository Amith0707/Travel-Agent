# Setting up dummy nodes for now
from .state import TravelState
from utils.logger import setup_logger
logger=setup_logger()


from modules.supervisor import decide_next_node

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
        state["query"]=query

        return state
    except Exception as e:
        print("ERROR in Node 1")
        logger.error(f"ERROR in Node 1: {e}")

def supervisor_route(state:TravelState)->str:
    try:
        '''Calling the brain of our workflow'''
        print("Entered the supervisor Node in workflow")
        logger.info("Entered the supervisor Node in workflow")

        result=decide_next_node(state) # Updated state goes in here

        return result.get("next_node") # This is a state as class is shared by all modules

    except Exception as e:
        print("ERROR in Node 2 Supervisor Node...")
        logger.error(f"ERROR in Node 2 Supervisor Node... :{e}")

    
    


def fetch_attractions(state):
    pass

def fetch_weather_data(state):
    pass

def filter_attractions(state):
    pass

def fetch_hotels(state):
    pass

def fetch_restaurants(state):
    pass

def generate_itinerary(state):
    pass

def currency_conversion(state):
    pass

def calculate_expenses(state):
    pass

def summarize(state):
    pass 