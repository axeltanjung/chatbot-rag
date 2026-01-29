from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # API Keys
    openrouter_api_key: str = "sk-or-v1-free"  # Free tier key
    
    # LLM Configuration
    # Free models available on OpenRouter:
    # - google/gemma-2-9b-it:free (Google's Gemma 2)
    # - meta-llama/llama-3.1-8b-instruct:free (Meta's Llama 3.1)
    # - mistralai/mistral-7b-instruct:free (Mistral 7B)
    llm_model: str = "google/gemma-2-9b-it:free"
    
    # Embedding model - using free alternative
    # Options:
    # - nomic-ai/nomic-embed-text-v1.5:free (768 dims, free)
    # - thenlper/gte-large:free (1024 dims, free)
    embedding_model: str = "thenlper/gte-large:free"
    embedding_dimension: int = 1024
    
    # OpenRouter API endpoint
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    # Vector Database
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "documents"
    anonymized_telemetry: bool = False
    
    # Chunking Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # RAG Configuration
    top_k: int = 5
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
