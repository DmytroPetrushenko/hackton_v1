import logging
import re
from googleapiclient.discovery import build
from langchain_core.messages import AIMessage

from constants import MESSAGES_ID, SENDERS, ERROR, PHISHING_IDS, PHISHING
from entities.launchers.launcher_bloodhound_graph import launcher_bloodhound_graph
from entities.states import PhishingState
from utily.gmail_utils import validate_and_generate, extract_email_body, forward_email_to_security, \
    move_email_to_phishing


def create_incoming_processor_node(state, name):
    """
    Node to process incoming emails.
    - Validates and generates the token.
    - Fetches list of new message IDs excluding processed and phishing labels.
    - Updates `state` with the message IDs and error messages if any.

    Args:
        state (dict): Shared state object;
        name (str): Node name or identifier;

    Returns:
        dict: A dictionary containing message IDs, sender information, and error (if any).
    """
    # Validation and token generation
    creds = validate_and_generate()
    service = build('gmail', 'v1', credentials=creds)

    try:
        # Request new emails without Processed and Phishing labels
        query = "-label:Processed -label:Phishing"
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            return {
                SENDERS: [name]
            }

        # Extract message IDs
        message_ids = [msg['id'] for msg in messages]

        # Return detailed dictionary
        return {
            MESSAGES_ID: set(message_ids),
            SENDERS: [name]
        }

    except Exception as e:
        logging.error(f"An error occurred in create_incoming_processor_node: {e}")
        return {
            SENDERS: [name],
            ERROR: [str(e)]  # Include an error message in the return dict
        }


def create_ai_processor_node(state: PhishingState, name: str):
    """
    Node for interacting with AI to analyze email content.

    Args:
        state (PhishingState): Shared state object;
        func (function): AI agent for email analysis;
        name (str): Node name or identifier;

    Returns:
        dict: Updated state with phishing IDs and any errors.

    """
    creds = validate_and_generate()
    service = build('gmail', 'v1', credentials=creds)

    phishing_ids = []
    errors = []

    try:
        # Retrieve message IDs from state
        message_ids = state.get(MESSAGES_ID, set())

        for message_id in message_ids:
            try:
                # Retrieve email content from Gmail API
                message = service.users().messages().get(userId='me', id=message_id, format='full').execute()

                # Extract subject, headers, and email body
                payload = message.get('payload', {})
                headers = payload.get('headers', [])
                parts = payload.get('parts', [])

                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "")
                email_body = extract_email_body(payload, parts)

                init_msg = f"Subject: {subject}\nEmail Body:\n {email_body}"

                # Send email details to AI agent for analysis
                # ai_result = agent.invoke({
                #     'messages': [AIMessage(content=init_msg)]
                # })

                ai_decision: str = launcher_bloodhound_graph(init_msg)


                # Classify based on AI response
                if re.search(re.compile(PHISHING), ai_decision):
                    phishing_ids.append(message_id)

            except Exception as e:
                logging.warning(f"Failed to process message ID {message_id}: {e}")
                errors.append(f"Error with message ID {message_id}: {e}")

        # Update state with results
        return {
            PHISHING_IDS: set(phishing_ids),
            SENDERS: [name],
            ERROR: errors,
        }

    except Exception as e:
        logging.error(f"An error occurred in AI Processor Node: {e}")
        return {
            PHISHING_IDS: set(),
            SENDERS: [name],
            ERROR: [str(e)]
        }



def create_outgoing_processor_node(state: PhishingState, name: str):
    """
        Processes outgoing phishing emails:
            - Marks emails as phishing by moving them to the 'Phishing' folder;
            - Forwards the emails to the Security Department;

        Args:
            state (PhishingState): Shared state object containing email IDs;
            name (str): Name or identifier of the node;

        Returns:
            dict: Updated state with sender information.
    """
    try:
        creds = validate_and_generate()
        service = build('gmail', 'v1', credentials=creds)

        phishing_ids = state.get(PHISHING_IDS, set())

        if not phishing_ids:
            logging.info("No phishing emails to process.")
            return {SENDERS: [name]}

        for current_id in phishing_ids:
            try:
                # Step 1: Mark the email as phishing
                move_email_to_phishing(service, current_id)

                # Step 2: Forward the email to the Security Department
                forward_email_to_security(service, current_id)

            except Exception as e:
                logging.error(f"Failed to process email with ID {current_id}: {e}")

        return {SENDERS: [name]}

    except Exception as e:
        logging.critical(f"Failed to initialize outgoing processor node: {e}")
        return {SENDERS: [name], ERROR: [str(e)]}




