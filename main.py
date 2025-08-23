# Streamlit Entry point
import os
from utils.logger import setup_logger
logger=setup_logger()
logger.info("This is the main file")

from graph.workflow import build_graph,mermaid_png

if __name__=="__main__":
    graph=build_graph()
    mermaid_png(graph)