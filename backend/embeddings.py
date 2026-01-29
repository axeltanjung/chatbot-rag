"""Embedding generation service using OpenRouter API."""

from typing import List
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings


class EmbeddingService:
    """Service for generating text embeddings using OpenRouter."""
    
    def __init__(self):
        """Initialize embedding service with OpenRouter client."""
        self.client = openai.OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url
        )
        self.model = settings.embedding_model
        self.dimension = settings.embedding_dimension
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "RAG Chatbot"
            }
        )
        return response.data[0].embedding
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 20) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts per API call (reduced for free tier)
            
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            response = self.client.embeddings.create(
                model=self.model,
                input=batch,
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "RAG Chatbot"
                }
            )
            
            # Extract embeddings in order
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
    
    def get_embedding_info(self) -> dict:
        """Get information about the embedding model."""
        return {
            'model': self.model,
            'dimension': self.dimension,
            'provider': 'OpenRouter (Free)'
        }
