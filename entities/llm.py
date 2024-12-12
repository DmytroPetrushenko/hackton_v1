from langchain_aws import ChatBedrock
from utily.enumerate_entities import MODEL


def creat_bedrock_llm(model_name: MODEL, region_name: str = "us-west-2"):
    llm = ChatBedrock(
        credentials_profile_name=None,
        model_id=model_name.value,
        region_name=region_name,
        streaming=True,
    )
    return llm


