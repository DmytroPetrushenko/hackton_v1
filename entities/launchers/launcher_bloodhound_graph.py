import logging

from langchain_core.messages import AIMessage

from constants import MESSAGES, SENDERS
from entities.graphs.bloodhound_graph import create_phishing_bloodhound
from entities.states import AIState


def launcher_bloodhound_graph(initial_message: str):
    """
    Launches the phishing email processing graph with PhishingState.
    Initializes the graph, compiles it, and invokes with a structured state.
    Includes logging for debugging and tracking.
    """
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Create the phishing graph
        logging.info("Creating the bloodhound graph...")
        phishing_graph = create_phishing_bloodhound()

        # Compile the graph
        logging.info("Compiling the bloodhound graph...")
        graph_compiled = phishing_graph.compile()

        initial_state = {
            MESSAGES: [AIMessage(content=initial_message)],
            SENDERS: ["Bloodhound Graph"]
        }

        # Invoke the graph with the initial state
        logging.info("Running the bloodhound graph...")
        evaluated: AIState = graph_compiled.invoke(initial_state)

        # Log the updated state after execution
        logging.info("Bloodhound Graph execution completed successfully.")
        logging.info(f"Updated state: {initial_state}")

        return evaluated.messages[-2].content

    except Exception as e:
        # Handle and log any exceptions during execution
        logging.error(f"Bloodhound Graph execution failed: {e}")
