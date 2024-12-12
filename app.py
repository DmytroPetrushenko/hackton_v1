import threading
import webbrowser

from flask import Flask, jsonify, render_template

from entities.launchers.launcher_phishing_graph import launcher_phishing_graph
from entities.states import PhishingState
from logger_config import logger, logs

app = Flask(__name__)
system_running = False


@app.route('/')
def index():
    """
    Render the main interface.
    """
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    """
    Starts the system if it is not already running.
    """
    global system_running
    if not system_running:
        system_running = True
        logs.append("System started.")
        logger.info("System started.")

        # Start graph execution in a separate thread
        threading.Thread(target=run_graphs_and_stop).start()
        return jsonify({"status": "Running"})
    return jsonify({"status": "Already running"})


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Returns the last 50 log entries.
    """

    return jsonify({"logs": logs[-50:]})


def run_graphs_and_stop():
    """
    Executes the graphs and stops the system afterward.
    """
    global system_running
    try:
        logger.info("Starting graph execution...")
        logs.append("Graph execution started.")

        # Execute the phishing graph
        run_graphs()

        # Stop the system after graph execution is complete
        logger.info("Graph execution completed. Stopping the system...")
        logs.append("Graph execution completed. System will stop.")
    except Exception as e:
        logger.error(f"Error during graph execution: {e}", exc_info=True)
        logs.append(f"Error during graph execution: {e}")
    finally:
        # Ensure the system stops even if there is an error
        system_running = False
        logs.append("System stopped.")
        logger.info("System stopped.")



def run_graphs():
    """
    Executes the phishing graph. Replace this function with your actual graph execution logic.
    """
    logger.info("Initializing graph execution...")

    # Define the initial state for the phishing graph
    initial_state: PhishingState = {
        "messages_id": set(),  # IDs of all messages (processed and unprocessed)
        "senders": [],  # Sources of incoming data
        "error": [],  # List of errors during processing
        "phishing_ids": set()  # IDs of detected phishing messages
    }

    logger.info(f"Initial state: {initial_state}")

    try:
        # Launch the phishing graph
        logger.info("Launching phishing graph...")
        launcher_phishing_graph(initial_state)

        # Log the updated state after execution
        logger.info(f"Graph execution completed. Final state: {initial_state}")
    except Exception as e:
        # Log any errors that occur during graph execution
        logger.error(f"An error occurred during graph execution: {e}", exc_info=True)


if __name__ == '__main__':
    # Automatically open the app in the default web browser
    port = 5001
    threading.Thread(target=lambda: webbrowser.open(f"http://127.0.0.1:{port}/")).start()
    app.run(debug=True, port=port)
