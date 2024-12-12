import operator
from typing import TypedDict, List, Annotated, Set, Literal

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from constants import PHISHING


class PhishingState(TypedDict):
    messages_id: Annotated[Set[str], operator.or_]  # IDs of all messages (processed and unprocessed)
    senders: Annotated[List[str], operator.add]  # Sources of incoming data
    error: Annotated[List[str], operator.add]  # List of errors during processing
    phishing_ids: Annotated[Set[str], operator.or_]  # IDs of messages classified as phishing


class AIState(BaseModel):
    messages: Annotated[List[BaseMessage], operator.add] = Field(default=list)  # List of messages to be processed
    senders: Annotated[List[str], operator.add] = Field(default=list)  # Sources of incoming data
    # noinspection PyTypeHints
    decision: Literal[PHISHING, "Clean", "No decision"] = Field(
        default="No decision",
        description="A schema representing the structure for validating a phishing detection agent's response."
    )
    explanation: str = Field(
        default='',
        description="The result of the validation. 'Repeat' if the response is invalid, 'Valid' if the response meets "
                    "the requirements."
    )
    validation: Literal["Repeat", "Valid"] = Field(
        default="Repeat",
        description="A schema representing the structure for validating a phishing detection agent's response.")
