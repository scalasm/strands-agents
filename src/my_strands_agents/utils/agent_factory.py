"""Utility functions for creating agent instances."""

import os

from strands.models.openai import OpenAIModel

DEFAULT_MODEL_ID = "gpt-4.1"
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TEMPERATURE = 0.7


def create_openai_model(
    model_id: str = DEFAULT_MODEL_ID,
    api_key: str | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> OpenAIModel:
    """
    Create an OpenAI model instance with the specified parameters.
    Parameters:
        model_id (str): The ID of the OpenAI model to use (default: "gpt-4.1").
        max_tokens (int): The maximum number of tokens to generate in the response (default: 1000).
        temperature (float): The sampling temperature for generating responses (default: 0.7).
    Returns:
        OpenAIModel: An instance of the OpenAIModel class configured with the specified parameters.
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API Key not passed and OPENAI_API_KEY environment variable is not set.")

    return OpenAIModel(
        client_args={
            "api_key": api_key,
        },
        model_id=model_id,
        params={
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
    )
