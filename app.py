import os
from utils.logger import setup_logger
logger=setup_logger()
# Creating a streamlit app from here
import streamlit as st
from datetime import datetime
#connecting to langgraph
from graph.nodes import get_user_input
from graph.state import TravelState
from graph.workflow import build_graph

st.set_page_config(page_title="AI Travel Agent", page_icon="🌍", layout="wide")

st.title("AI Travel Agent & Expense Planner")

with st.form("user_inputs"):
    col1, col2 = st.columns(2)
    with col1:
        current_city = st.text_input("Your Current City", placeholder="e.g., Mumbai")
        destination_city = st.text_input("Destination City", placeholder="e.g., Paris")
    with col2:
        start_date = st.date_input("Travel Start Date", min_value=datetime.today())
        end_date = st.date_input("Travel End Date", min_value=datetime.today())
    
    hotel_budget = st.number_input("Hotel Budget per Night (in your currency)", min_value=100, step=50)
    travel_budget = st.number_input("Maximum Budget of your trip(in your currency)", min_value=10000, step=50)
    
    submitted = st.form_submit_button("Plan My Trip 🚀")

if submitted:
    st.success("Inputs received! Passing to AI agent...")
    
    user_inputs = {
        "current_city": current_city,
        "destination_city": destination_city,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "hotel_budget": hotel_budget,
        "travel_budget":travel_budget
    }


    st.write(" Collected Inputs:", user_inputs)
    logger.info("Collected User input..")
    print("Collected User input..")
    
    state:TravelState=TravelState()
    state["user_input"]=user_inputs

    logger.info("Initalizing and compiling the Graph...")
    logger.error("Initalizing and compiling the Graph...")
    
    workflow=build_graph()# Returns a compiled stategraph (workflow.compile())
    logger.info("Compiled the graph successfully..")
    print("Compiled the graph successfully..")

    logger.info("Running the graph now.....")
    print("Running the graph now.....")
    # workflow.run(state) doesnt work as CompiledStateGraph doesnt has this method
    final_state=workflow.execute("START",state)
    st.write("Final Travel State:", final_state)
    st.write("Supervisor decided next node:", final_state.get("next_node"))
    logger.info(f"Supervisor routed to: {final_state.get('next_node')}")    