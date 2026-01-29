"""RAG engine orchestrating retrieval and generation."""

from typing import List, Dict, Optional
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings
from embeddings import EmbeddingService
from vector_store import VectorStore
from prompts import build_rag_prompt, get_prompt_for_display
from models import Source, ChatResponse


class RAGEngine:
    """Orchestrates RAG pipeline: retrieval + generation."""
    
    def __init__(self):
        """Initialize RAG engine with dependencies."""
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_client = openai.OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url
        )
        self.llm_model = settings.llm_model
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _call_llm(self, messages: List[Dict]) -> str:
        """
        Call LLM with retry logic.
        
        Args:
            messages: Chat messages
            
        Returns:
            LLM response text
        """
        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=messages,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "RAG Chatbot"
            }
        )
        return response.choices[0].message.content
    
    def query(
        self, 
        query: str, 
        chat_history: List[Dict] = None,
        top_k: int = None,
        include_prompt: bool = False
    ) -> ChatResponse:
        """
        Process a query using RAG.
        
        Args:
            query: User's question
            chat_history: Optional conversation history
            top_k: Number of chunks to retrieve
            include_prompt: Whether to include prompt in response (developer mode)
            
        Returns:
            ChatResponse with answer, sources, and confidence
        """
        if top_k is None:
            top_k = settings.top_k
        
        # Step 1: Convert query to embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Step 2: Retrieve relevant chunks
        retrieved_chunks = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k
        )
        
        # Handle empty retrieval
        if not retrieved_chunks:
            return ChatResponse(
                answer="I don't have any documents indexed yet. Please upload some documents first.",
                sources=[],
                confidence=0.0,
                prompt_used=None
            )
        
        # Step 3: Build prompt with context
        messages = build_rag_prompt(query, retrieved_chunks, chat_history)
        
        # Step 4: Generate answer
        answer = self._call_llm(messages)
        
        # Step 5: Format sources
        sources = [
            Source(
                chunk_id=chunk['chunk_id'],
                text=chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                source=chunk['metadata'].get('source', 'Unknown'),
                page=chunk['metadata'].get('page') if chunk['metadata'].get('page', -1) != -1 else None,
                similarity_score=round(chunk['similarity_score'], 4)
            )
            for chunk in retrieved_chunks
        ]
        
        # Step 6: Calculate confidence score
        confidence = self._calculate_confidence(retrieved_chunks)
        
        # Step 7: Prepare response
        prompt_used = None
        if include_prompt:
            prompt_used = get_prompt_for_display(messages)
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            prompt_used=prompt_used
        )
    
    def _calculate_confidence(self, chunks: List[Dict]) -> float:
        """
        Calculate confidence score based on retrieval quality.
        
        Heuristic approach:
        - Average similarity score of top chunks
        - Weighted more heavily toward top results
        
        Args:
            chunks: Retrieved chunks with similarity scores
            
        Returns:
            Confidence score between 0 and 1
        """
        if not chunks:
            return 0.0
        
        # Weight scores: top result gets more weight
        weights = [1.0 / (i + 1) for i in range(len(chunks))]
        total_weight = sum(weights)
        
        weighted_score = sum(
            chunk['similarity_score'] * weight 
            for chunk, weight in zip(chunks, weights)
        ) / total_weight
        
        # Normalize to 0-1 range
        confidence = max(0.0, min(1.0, weighted_score))
        
        return round(confidence, 4)
