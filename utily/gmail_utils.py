import base64
import logging
import os
import pickle
from base64 import urlsafe_b64decode
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from constants import PHISHING_LABEL, SECURITY_MAIL

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]


def validate_and_generate(token_file='token.pickle', credentials_file='credentials.json'):
    """
    Validate, refresh, or generate a new token.
    """
    creds = None

    # Check if a token file exists
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # Refresh the token if it is expired
    if creds and creds.expired and creds.refresh_token:
        print("Refreshing access token...")
        creds.refresh(Request())
    # Generate a new token if no valid token exists
    elif not creds or not creds.valid:
        print("No valid token found. Generating a new one...")
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the updated token to a file
    with open(token_file, 'wb') as token:
        pickle.dump(creds, token)

    return creds


def list_emails():
    creds = validate_and_generate()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    for message in messages:
        print(f"Message ID: {message['id']}")


def extract_email_body(payload, parts):
    """
    Extracts the email body from the message payload.

    Args:
        payload (dict): The top-level payload of the email.
        parts (list): The list of parts in the email payload.

    Returns:
        str: The extracted and decoded email body.
    """
    try:
        # If the body exists directly in payload
        body = payload.get('body', {}).get('data', '')
        if body:
            return decode_base64(body)

        # If the body is split into parts, extract from text/plain or text/html
        for part in parts:
            mime_type = part.get('mimeType', '')
            part_body = part.get('body', {}).get('data', '')

            if mime_type == 'text/plain' and part_body:
                return decode_base64(part_body)
            elif mime_type == 'text/html' and part_body:
                return decode_base64(part_body)

        # Return empty string if no content found
        return ''
    except Exception as e:
        logging.warning(f"Failed to extract email body: {e}")
        return ''


def decode_base64(data):
    """
    Decodes Base64-encoded string from Gmail API.

    Args:
        data (str): Base64-encoded string.

    Returns:
        str: Decoded string.
    """
    try:
        return urlsafe_b64decode(data).decode('utf-8')
    except Exception as e:
        logging.warning(f"Failed to decode Base64 content: {e}")
        return ''


def check_or_create_phishing_label(service):
    """
    Creates a new label in Gmail if it doesn't exist.

    Args:
        service: Gmail API service instance.
        label_name: Name of the label to create.

    Returns:
        str: The ID of the label.
    """
    # Get all existing labels
    labels = service.users().labels().list(userId='me').execute().get('labels', [])

    # Check if the label already exists
    for label in labels:
        if label['name'] == PHISHING_LABEL:
            return label['id']

    # Create a new label
    label_body = {
        "name": PHISHING_LABEL,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    created_label = service.users().labels().create(userId='me', body=label_body).execute()
    return created_label['id']


def move_email_to_phishing(service, message_id):
    """
    Moves an email to the 'Phishing' label by adding the label and removing 'INBOX'.

    Args:
        service: Gmail API service instance.
        message_id: ID of the email to move.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    phishing_label_id = check_or_create_phishing_label(service)

    try:
        # Modify the message labels
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={
                "addLabelIds": [phishing_label_id],  # Add the 'Phishing' label
                "removeLabelIds": ["INBOX"]  # Remove it from 'INBOX'
            }
        ).execute()

        logging.info(f"Message {message_id} moved to 'Phishing' folder.")
        return True

    except Exception as e:
        logging.error(f"Failed to move message {message_id} to 'Phishing': {str(e)}")
        return False


def forward_email_to_security(service, message_id):
    """
    Forwards a suspicious email to the Security Department.

    Args:
        service: Gmail API service instance.
        message_id: ID of the email to forward.

    Returns:
        bool: True if the email was forwarded successfully, False otherwise.
    """
    try:
        # Step 1: Retrieve the original email in raw format
        message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()

        # Step 2: Extract the raw email data
        raw_email = message.get('raw', '')

        if not raw_email:
            logging.error(f"Failed to retrieve raw email for message ID {message_id}.")
            return False

        # Step 3: Send the email to the Security Department
        service.users().messages().send(
            userId='me',
            body={
                'raw': raw_email,
                'to': SECURITY_MAIL
            }
        ).execute()

        logging.info(f"Email with ID {message_id} successfully forwarded to {SECURITY_MAIL}.")
        return True

    except Exception as e:
        logging.error(f"Failed to forward email with ID {message_id} to {SECURITY_MAIL}: {str(e)}")
        return False
