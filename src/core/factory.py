import os
from dotenv import load_dotenv
from src.core.llm_provider import LLMProvider
from src.core.openai_provider import OpenAIProvider
from src.core.gemini_provider import GeminiProvider
from src.core.local_provider import LocalProvider

def get_provider() -> LLMProvider:
    """
    Factory function to get the LLM provider based on environment variables.
    Seamlessly swaps between OpenAI, Gemini, and Local models.
    """
    load_dotenv()
    
    provider_name = os.getenv("DEFAULT_PROVIDER", "openai").lower()
    model_name = os.getenv("DEFAULT_MODEL")
    
    if provider_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")
        if not model_name:
            model_name = "gpt-4o"
        return OpenAIProvider(model_name=model_name, api_key=api_key)
        
    elif provider_name == "google" or provider_name == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        if not model_name:
            model_name = "gemini-1.5-flash"
        return GeminiProvider(model_name=model_name, api_key=api_key)
        
    elif provider_name == "local":
        model_path = os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf")
        return LocalProvider(model_path=model_path)
        
    else:
        raise ValueError(f"Unknown provider configured: {provider_name}")
