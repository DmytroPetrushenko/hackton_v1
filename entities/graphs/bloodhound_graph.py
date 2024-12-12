import functools

from langgraph.constants import END
from langgraph.graph import StateGraph

from constants import SNIFFER, CHECKER
from entities.agents import agent_without_tools, agent_constructed_output
from entities.llm import creat_bedrock_llm, create_llm
from entities.nodes import create_ordinary_node
from entities.routers import checker_router
from entities.states import AIState
from utily.common import create_message_from_file
from utily.enumerate_entities import MODEL


def create_phishing_bloodhound() -> StateGraph:
    # create an agent
    # claude_llm = creat_bedrock_llm(model_name=MODEL.ANTROPIC_CLAUDE_3_5_SONNET)
    claude_llm = create_llm(model_name='claude 3.5 Sonnet')

    phishing_prompt = create_message_from_file('prompts/phishing#1.txt')
    sniffer_agent = agent_without_tools(model_llm=claude_llm, prompt=phishing_prompt)

    mistral_llm = creat_bedrock_llm(model_name=MODEL.MISTRAL_LARGE)
    checker_prompt = create_message_from_file('prompts/checker#1.txt')
    checker_agent = agent_without_tools(model_llm=mistral_llm, prompt=checker_prompt)

    # Nodes
    sniffer_node = functools.partial(create_ordinary_node, agent=sniffer_agent, name=SNIFFER)
    checker_node = functools.partial(create_ordinary_node, agent=checker_agent, name=CHECKER)

    graph = StateGraph(AIState)

    graph.add_node(SNIFFER, sniffer_node)
    graph.add_node(CHECKER, checker_node)

    graph.set_entry_point(SNIFFER)
    graph.add_edge(SNIFFER, CHECKER)
    graph.add_conditional_edges(
        CHECKER,
        checker_router,
        {
            END: END,
            SNIFFER: SNIFFER
        }
    )

    return graph
