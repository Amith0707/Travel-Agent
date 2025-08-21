# To define AgentState or Messages state that we want to pass around

#This is a different way we are making compared to the agentstatre that I learnt as agentstate is flexible than messages state

from typing import TypedDict,List,Dict

class TravelState(TypedDict,total=False):
    user_input:Dict
    attractions:List[str]
    weather:Dict
    filtered_attractions:List[str]
    hotels:List[Dict]
    restaurants:List[Dict] #-->add into workflow later
    itinerary:List[str]
    converted_curreny:Dict
    expenses:Dict
    summary:str