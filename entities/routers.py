import re

from langgraph.constants import END

from constants import SNIFFER
from entities.states import AIState


def checker_router(state: AIState):
    if state.validation == "Valid":
        return END
    return SNIFFER
