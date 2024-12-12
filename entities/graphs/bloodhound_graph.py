import functools

from langgraph.constants import END
from langgraph.graph import StateGraph

from constants import SNIFFER, CHECKER
from entities.agents import agent_constructed_output
from entities.llm import create_llm
from entities.nodes import create_sniffer_node, create_checker_node
from entities.routers import checker_router
from entities.schemes import phishing_response_schema, checker_response_schema
from entities.states import AIState
from utily.common import create_message_from_file
from utily.enumerate_entities import MODEL


def create_phishing_bloodhound() -> StateGraph:
    claude_llm = create_llm(model_name=MODEL.AWS_CLAUDE_35_SONNET_V2)
    phishing_prompt = create_message_from_file('prompts/phishing#1.txt')
    sniffer_agent = agent_constructed_output(
        model_llm=claude_llm,
        prompt=phishing_prompt,
        output_scheme=phishing_response_schema
    )

    mistral_llm = create_llm(model_name=MODEL.AWS_MISTRAL_LARGE)
    checker_prompt = create_message_from_file('prompts/checker#1.txt')
    checker_agent = agent_constructed_output(
        model_llm=mistral_llm,
        prompt=checker_prompt,
        output_scheme=checker_response_schema
    )

    # Nodes
    sniffer_node = functools.partial(create_sniffer_node, agent=sniffer_agent, name=SNIFFER)
    checker_node = functools.partial(create_checker_node, agent=checker_agent, name=CHECKER)

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
