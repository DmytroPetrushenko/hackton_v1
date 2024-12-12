import re

from langgraph.constants import END

from constants import SNIFFER
from entities.states import AIState


def checker_router(state: AIState):
    last_messages = state.messages[-1]

    condition = re.compile('repeat',  re.IGNORECASE)

    if re.search(condition, last_messages.content):
        return SNIFFER

    return END
