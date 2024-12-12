from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_aws import ChatBedrock


def agent_without_tools(
        model_llm: ChatBedrock,
        prompt: str
):
    """
    Creates an agent that operates without tools.

    Args:
        model_llm (ChatBedrock): The language model to use for the agent;
        prompt (str): The system-level prompt for the agent;

    Returns:
        ChatPromptTemplate: A prompt template bound to the specified language model.
    """
    try:
        # Define the prompt list with system message and placeholder for messages
        prompt_list = [
            ("system", prompt),
            MessagesPlaceholder(variable_name="messages")
        ]

        # Build the chat prompt template from the defined prompt list
        chat_prompt = ChatPromptTemplate.from_messages(prompt_list)

        # Bind the prompt to the language model
        agent = chat_prompt | model_llm

        return agent
    except Exception as e:
        # Raise an error with a clear message in case of failure
        raise ValueError(f"Error creating the agent without tools: {e}")
