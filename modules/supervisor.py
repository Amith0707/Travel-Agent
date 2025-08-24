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
    prompt = ChatPromptTemplate([
        ("system", TEMPLATE),
        ("human", "User query:\n{user_input}\n\nCurrent state snapshot:\n{snapshot}")
    ])
    print("LLM Initalized Successfully")
    logger.info("LLM Initalized Successfully")

    chain=prompt|llm #------->Chaining here

except Exception as e:
    print("Error occured in Supervisor.py")
    logger.error("Error occured in Supervisor.py",e)
####################################################################
# Brain of my workflow 
def decide_next_node(state: TravelState) -> TravelState:
    try:
        print("Entered decide_next_node in supervisor.py")
        logger.info("Entered decide_next_node in supervisor.py")

        # Step 1: Collect user query + minimal state snapshot
        query = state.get("query", "")
        snapshot = {
            "filtered_attractions": state.get("filtered_attractions", []),
            "itinerary": state.get("itinerary", []),
            "hotels": state.get("hotels", []),
            "restaurants": state.get("restaurants", []),
            "summary": state.get("summary", ""),
            "hotel_loop_count": state.get("hotel_loop_count", 0)
        }
        # Send snapshot + query into the LLM
        response = chain.invoke({
            "user_input": query,
            "snapshot": snapshot
        })

        llm_output = response.content.strip()
        print(f"LLM Raw Response: {llm_output}")
        logger.info(f"LLM Raw Response: {llm_output}")

        # Step 2: Parse and validate routing
        VALID_KEYS = ["activities", "hotels", "currency", "summarizer", "end"]
        next_node = llm_output if llm_output in VALID_KEYS else "error"

        print(f"Supervisor routed to: {next_node}")
        logger.info(f"Supervisor routed to: {next_node}")

        # Step 3: Update state
        state["next_node"] = next_node
        # Force hotel to appear only once
        hotel_count = state.get("hotel_loop_count", 0)
        if next_node == "hotels":
            if hotel_count >= 1:           # already visited once
                state["next_node"] = "currency"  # force next
            else:
                state["hotel_loop_count"] = hotel_count + 1
        else:
            state["hotel_loop_count"] = 0   # reset if moving out of hotels

        return state

    except Exception as e:
        print("Error in decide_next_node..", e)
        logger.error("Error in decide_next_node..", exc_info=True)
        state["next_node"] = "error"
        return state
