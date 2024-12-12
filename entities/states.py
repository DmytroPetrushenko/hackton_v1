import operator
from typing import TypedDict, List, Annotated, Set


class PhishingState(TypedDict):
    messages_id: Annotated[Set[str], operator.or_]  # IDs of all messages (processed and unprocessed)
    senders: Annotated[List[str], operator.add]      # Sources of incoming data
    error: Annotated[List[str], operator.add]        # List of errors during processing
    phishing_ids: Annotated[Set[str], operator.or_]  # IDs of messages classified as phishing
