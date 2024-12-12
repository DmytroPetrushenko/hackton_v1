import logging

# Global logs array for UI
logs = []


class UIHandler(logging.Handler):
    """
    Custom logging handler to store logs in the global `logs` array.
    """

    def emit(self, record):
        log_entry = self.format(record)
        logs.append(log_entry)
        # Limit the size of logs to avoid memory overflow
        if len(logs) > 1000:
            logs.pop(0)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Logs to console
        UIHandler()  # Logs to the global `logs` array
    ]
)

# Access the logger globally
logger = logging.getLogger(__name__)
logging.getLogger('werkzeug').disabled = True
