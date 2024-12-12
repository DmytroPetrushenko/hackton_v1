from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_aws import ChatBedrock, ChatBedrockConverse
from utily.enumerate_entities import MODEL
from utily.litteral_entites import MODEL_L


def _creat_bedrock_llm(model_name: MODEL, temperature, region_name: str = "us-west-2"):
    llm = ChatBedrockConverse(
        credentials_profile_name=None,
        model_id=model_name.value,
        region_name=region_name,
        temperature=temperature

    )
    return llm


def _creat_antropic_llm(model_name: MODEL, temperature):
    llm = ChatAnthropic(
        model_name=model_name,
        temperature=temperature,
        max_tokens=1024
    )
    return llm


def create_llm(model_name: MODEL, temperature: float = 0.001):
    """
    Creates a language model instance based on the provided model name.

    Args:
        model_name (MODEL): An enum or class representing the model type.
        temperature (float): The temperature setting for the model (default is 0).

    Returns:
        Union[ChatBedrock, ChatAnthropic, ChatOpenAI]: An instance of the selected LLM.

    Raises:
        ValueError: If the model name is not recognized or unsupported.
    """
    try:
        if model_name.name.startswith("AWS"):
            llm = _creat_bedrock_llm(model_name, temperature)
        elif model_name.name.startswith("ANTHROPIC"):
            llm = _creat_antropic_llm(model_name, temperature)
        else:
            raise ValueError(f"Unsupported model name: {model_name.name}")

        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to create LLM for model {model_name.name}: {str(e)}")

