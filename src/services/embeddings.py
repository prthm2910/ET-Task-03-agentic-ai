from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.core.config import settings


def get_embeddings_provider():
    """Factory to get the embedding provider."""
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
        output_dimensionality=settings.embedding_dimensions
    )
