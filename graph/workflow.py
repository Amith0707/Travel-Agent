# Graph to get the skeleton of our project
#Importing the necessary libraries

import os
from utils.logger import setup_logger
logger=setup_logger()
from langgraph.graph import StateGraph,END,START
from langgraph.graph.state import CompiledStateGraph
from IPython.display import Image,display
from . import nodes #Importing functions from node.py
from .state import TravelState #-->Importing the class

def build_graph()->CompiledStateGraph:
    logger.info("Entered the Graph Builder of our workflow")
    print("Entered the Graph Builder of our workflow")

    #Initalized the graph
    workflow=StateGraph(TravelState)

    logger.info("Creating Nodes..")
    print("Creating Nodes..")
    # Adding Nodes
    workflow.add_node("User Input",nodes.get_user_input)
    workflow.add_node("Supervisor",nodes.supervisor_route)
    workflow.add_node("Fetch Attractions",nodes.fetch_attractions)
    workflow.add_node("Fetch Weather",nodes.fetch_weather_data)
    workflow.add_node("Filter Activities",nodes.filter_attractions)
    workflow.add_node("Hotels",nodes.fetch_hotels)
    workflow.add_node("Restaurants",nodes.fetch_restaurants)
    workflow.add_node("Itinerary Planner",nodes.generate_itinerary)
    workflow.add_node("Currency Converter",nodes.currency_conversion)
    workflow.add_node("Summarizer",nodes.summarize)

    logger.info("Nodes Generated successfully..")
    print("Nodes Generated successfully..")

    logger.info("Creating Edges...")
    print("Creating Edges...")
    # Connecting the edges
    logger.info("Creating Edges...")
    print("Creating Edges...")

    # Entry
    workflow.add_edge(START, "User Input")
    workflow.add_edge("User Input", "Supervisor")

    # Conditional routing from Supervisor
    workflow.add_conditional_edges(
        "Supervisor",
        lambda state:state.get("next_node","end"),  # this must return a key like "activities", "hotels"
        {
            "activities": "Fetch Attractions",
            "hotels": "Hotels",
            "currency": "Currency Converter",
            "summarizer": "Summarizer"
            # "end": END,
        }
    )

    # Activities branch
    workflow.add_edge("Fetch Attractions", "Fetch Weather")
    workflow.add_edge("Fetch Weather", "Filter Activities")
    workflow.add_edge("Filter Activities", "Supervisor")

    # Hotels branch
    workflow.add_edge("Hotels", "Restaurants")
    workflow.add_edge("Restaurants", "Itinerary Planner")
    workflow.add_edge("Itinerary Planner", "Supervisor")

    # Currency branch
    workflow.add_edge("Currency Converter", "Summarizer")
    workflow.add_edge("Summarizer",END)


    logger.info("Edges Created..")
    print("Edges Created..")
    app=workflow.compile()
    return app

def mermaid_png(graph:CompiledStateGraph):
    """Function to generate the workflow graph"""
    filename="artifacts/graph.png"
     #time to save the image
    os.makedirs(os.path.dirname(filename),exist_ok=True)

    png_bytes=graph.get_graph().draw_mermaid_png()

    with open(filename,"wb") as f:
        f.write(png_bytes)

    logger.info(f"Saved the Graph IMage at {filename}")
    print(f"Saved the Graph IMage at {filename}")

# if __name__=="__main__":
#     res=build_graph()
#     mermaid_png(res)