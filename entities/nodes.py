from langchain_core.messages import HumanMessage

from constants import MESSAGES, SENDERS, DECISION, EXPLANATION, VALIDATION
from entities.states import AIState


def create_sniffer_node(state: AIState, agent, name):
    messages = [state.messages[-1]]
    response = agent.invoke({MESSAGES: [HumanMessage(content=messages[-1].content)]})

    return {
        DECISION: response.get(DECISION, 'No decision'),
        EXPLANATION: response.get(EXPLANATION, 'No explanations!'),
        SENDERS: [name]
    }


def create_checker_node(state: AIState, agent, name):
    message = f'decision: {state.decision},  explanation: {state.explanation}'
    response = agent.invoke({MESSAGES: [HumanMessage(content=message)]})

    return {
        VALIDATION: response.get(VALIDATION, 'Repeat'),
        SENDERS: [name]
    }
