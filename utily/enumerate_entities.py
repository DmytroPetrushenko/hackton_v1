from enum import Enum


class MODEL(Enum):
    # LLAMA_90B_VISION = "meta.llama3-2-90b-instruct-v1:0"
    MISTRAL_LARGE = "mistral.mistral-large-2402-v1:0"
    LLAMA_31_405B_INSTRUCT = "meta.llama3-1-405b-instruct-v1:0"
    CLAUDE_3_5_SONNET_2 = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    CLAUDE_3_5_SONNET = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    ANTROPIC_CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
