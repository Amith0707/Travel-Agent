import os
from dotenv import load_dotenv
load_dotenv()
from utils.logger import setup_logger
logger=setup_logger()

from utils.constants import TEMPLATE,OPENAI_MODEL

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.state import TravelState

try:      
    api_key=os.getenv("OPENAI_API_KEY")
    model=OPENAI_MODEL
    llm=ChatOpenAI(api_key=api_key,model=model,temperature=0)

    # Setting up the prompt
    prompt=ChatPromptTemplate([#-->fully crct
        ("system",TEMPLATE),
        ("human","{user_input}")
        ])
    print("LLM Initalized Successfully")
    logger.info("LLM Initalized Successfully")

    chain=prompt|llm #------->Chaining here

except Exception as e:
    print("Error occured in Supervisor.py")
    logger.error("Error occured in Supervisor.py",e)
####################################################################
# Brain of my workflow 
def decide_next_node(state:TravelState)->TravelState:
    try:
            
        """Decides which node to call next in the flow based on TravelState data it has."""
        # Step 1 is to take the user input
        query=state.get("query","") # ""->means returns empty string if query is empty
        response=chain.invoke({"user_input":query})
        print(response.content)
        print("\n LLM Response Generated successfully..")
        logger.info("LLM Response Generated successfully..")

        next_node=response.content.strip()
        print(f"Supervisor routed to: {next_node}")
        logger.info(f"Supervisor routed to: {next_node}")

        # For safety
        VALID_NODES = [
            "User Input", "Supervisor","Fetch Attractions", "Fetch Weather", 
            "Filter Activities","Hotels", "Restaurants", "Itinerary Planner", 
            "Currency Converter","Summarizer"
        ]

        if next_node not in VALID_NODES:
            next_node = "error"
        
        #Updating the next_node
        state["next_node"]=next_node

        return state

    except Exception as e:
        print("Error in decide_next_node..")
        logger.error("Error in decide_next_node..",e)