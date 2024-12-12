import functools

from langgraph.graph import StateGraph

from constants import INCOMING_PROCESSOR, AI_PROCESSOR, OUTGOING_PROCESSOR
from entities.agents import agent_without_tools
from entities.llm import creat_bedrock_llm
from entities.nodes import create_incoming_processor_node, create_ai_processor_node, create_outgoing_processor_node
from entities.states import PhishingState
from utily.common import create_message_from_file
from utily.enumerate_entities import MODEL

state = {
    "history_que": [],  # History of processed historyId
    "messages_id": []   # List of new message IDs
}


def create_phishing_graph() -> StateGraph:
    """
    Creates the phishing email processing graph.

    This graph is responsible for handling the flow of phishing email detection
    and processing. It initializes the graph, sets entry and finish points,
    and includes the necessary nodes for processing.

    Returns:
        graph (StateGraph): Configured phishing email processing graph.
    """

    # create an agent
    mistral_llm = creat_bedrock_llm(model_name=MODEL.MISTRAL_LARGE)
    prompt = create_message_from_file('prompts/phishing#1.txt')
    agent = agent_without_tools(model_llm=mistral_llm, prompt=prompt)

    # Create incoming processor node
    incoming_processor_node = functools.partial(create_incoming_processor_node, name=INCOMING_PROCESSOR)

    ai_processor_node = functools.partial(create_ai_processor_node, agent=agent, name=AI_PROCESSOR)

    outgoing_processor_node = functools.partial(create_outgoing_processor_node, name=OUTGOING_PROCESSOR)

    # Initialize the state graph with the specified state class (PhishingState)
    graph = StateGraph(PhishingState)


    graph.add_node(INCOMING_PROCESSOR, incoming_processor_node)
    graph.add_node(AI_PROCESSOR, ai_processor_node)
    graph.add_node(OUTGOING_PROCESSOR, outgoing_processor_node)


    graph.set_entry_point(INCOMING_PROCESSOR)
    graph.add_edge(INCOMING_PROCESSOR, AI_PROCESSOR)
    graph.add_edge(AI_PROCESSOR, OUTGOING_PROCESSOR)
    graph.set_finish_point(OUTGOING_PROCESSOR)

    # Return the configured graph
    return graph



