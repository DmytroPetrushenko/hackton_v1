from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_aws import ChatBedrock
from utily.enumerate_entities import MODEL
from utily.litteral_entites import MODEL_L


def creat_bedrock_llm(model_name: MODEL, region_name: str = "us-west-2"):
    llm = ChatBedrock(
        credentials_profile_name=None,
        model_id=model_name.value,
        region_name=region_name,
        streaming=True,
    )
    return llm


def creat_antropic_llm(model_name: MODEL):
    llm = ChatAnthropic(
        model_name=model_name,
        temperature=0,
        max_tokens=1024
    )
    return llm


def get_correct_anthropic_name(model_name: str) -> Optional[str]:
    if model_name == 'claude 3.5 Sonnet':
        return 'claude-3-5-sonnet-20240620'
    if model_name == 'claude 3 Sonnet':
        return 'claude-3-sonnet-20240229'
    if model_name == 'claude 3 Opus':
        return 'claude-3-opus-20240229'
    return None


def get_correct_bedrock_name(model_name):
    if model_name == 'aws Claude 3.5 Sonnet v2':
        return 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
    if model_name == 'aws Claude 3.5 Sonnet v1':
        return 'anthropic.claude-3-5-sonnet-20240620-v1:0'
    if model_name == 'aws Claude 3 Haiku':
        return 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
    return None


def create_llm(model_name: MODEL_L, temperature: float = 0) -> ChatOpenAI:
    if 'gpt' in model_name:
        llm = ChatOpenAI(model=model_name, temperature=temperature)
    elif 'claude' in model_name.lower():
        correct_anthropic_name = get_correct_anthropic_name(model_name)
        llm = ChatAnthropic(model_name=correct_anthropic_name, temperature=temperature)
    elif 'aws' in model_name.lower():
        correct_bedrock_name = get_correct_bedrock_name(model_name)
        llm = ChatBedrock(model_name=correct_bedrock_name, temperature=temperature)
    else:
        raise ValueError('model_name doesn\'t exist as a key in the following list: \'gpt\', \'claude\'')
    return llm
