# To define AgentState or Messages state that we want to pass around

#This is a different way we are making compared to the agentstatre that I learnt as agentstate is flexible than messages state

from typing import TypedDict,List,Dict

class TravelState(TypedDict,total=False):
    query:str
    user_input:Dict
    attractions:List[Dict] #-->serper gives output in json
    weather:Dict
    filtered_attractions:List[str]
    hotels:List[Dict]
    restaurants:List[Dict] #-->add into workflow later
    itinerary:List[str]
    from_curreny:str
    to_currency:str
    exchange_value:float
    summary:str
    next_node:str #->decides which node to call next
    hotel_loop_count:int