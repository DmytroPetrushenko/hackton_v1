from constants import MESSAGES, SENDERS, CHECKER
from entities.states import AIState


def create_ordinary_node(state: AIState, agent, name):

    messages = [state.messages[-1]]
    response = agent.invoke({MESSAGES: messages})


    return {
        MESSAGES: [response],
        SENDERS: [name]
    }