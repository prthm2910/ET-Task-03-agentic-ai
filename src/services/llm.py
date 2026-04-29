from langchain_openai import ChatOpenAI

from src.core.config import settings


def get_chat_model(is_flash=False):
    """Factory to get the requested LLM provider."""
    model = settings.flash_model_name if is_flash else settings.model_name
    return ChatOpenAI(
        model=model,
        api_key=settings.nvidia_api_key,
        base_url=settings.nim_base_url,
        temperature=0
    )
