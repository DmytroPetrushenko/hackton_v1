import logging

from entities.graphs.bloodhound_graph import create_phishing_bloodhound
from entities.graphs.phishing_graph import create_phishing_graph
from entities.states import PhishingState, AIState


def launcher_phishing_graph(initial_state: PhishingState):
    """
    Launches the phishing email processing graph with PhishingState.
    Initializes the graph, compiles it, and invokes with a structured state.
    Includes logging for debugging and tracking.
    """
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Create the phishing graph
        logging.info("Creating the phishing graph...")
        phishing_graph = create_phishing_graph()

        # Compile the graph
        logging.info("Compiling the phishing graph...")
        graph_compiled = phishing_graph.compile()

        # Invoke the graph with the initial state
        logging.info("Running the phishing graph...")
        evaluated = graph_compiled.invoke(initial_state)

        # Log the updated state after execution
        logging.info("Graph execution completed successfully.")
        logging.info(f"Updated state: {initial_state}")

        return evaluated

    except Exception as e:
        # Handle and log any exceptions during execution
        logging.error(f"Graph execution failed: {e}")
