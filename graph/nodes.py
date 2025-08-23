# Setting up dummy nodes for now
from .state import TravelState
from utils.logger import setup_logger
logger=setup_logger()
from modules.supervisor import decide_next_node # Supervisor Node
from modules.attractions import get_attractions #seper call to get attractions

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

def fetch_weather_data(state):
    print("="*50)
    print("ENtered weather node")

def filter_attractions(state):
    print("="*50)
    print("ENtered Filter Attractions node")


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