"""Smoke tests for retrieval quality."""

import pytest
from backend.embeddings import EmbeddingService
from backend.vector_store import VectorStore
from backend.models import DocumentChunk, ChunkMetadata
from backend.config import settings
import os


# Skip tests if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv('OPENAI_API_KEY'),
    reason="OPENAI_API_KEY not set"
)


@pytest.fixture
def embedding_service():
    """Create embedding service instance."""
    return EmbeddingService()


@pytest.fixture
def vector_store():
    """Create vector store instance."""
    # Use test collection
    original_collection = settings.chroma_collection_name
    settings.chroma_collection_name = "test_collection"
    
    store = VectorStore()
    yield store
    
    # Cleanup
    store.clear_collection()
    settings.chroma_collection_name = original_collection


def test_retrieval_relevance(embedding_service, vector_store):
    """Test that retrieval returns relevant chunks."""
    
    # Create test documents
    chunks = [
        DocumentChunk(
            chunk_id="1",
            text="Python is a high-level programming language known for its simplicity.",
            metadata=ChunkMetadata(source="python.txt", chunk_id="1")
        ),
        DocumentChunk(
            chunk_id="2",
            text="JavaScript is primarily used for web development and runs in browsers.",
            metadata=ChunkMetadata(source="javascript.txt", chunk_id="2")
        ),
        DocumentChunk(
            chunk_id="3",
            text="Machine learning is a subset of artificial intelligence.",
            metadata=ChunkMetadata(source="ml.txt", chunk_id="3")
        ),
    ]
    
    # Generate embeddings
    texts = [chunk.text for chunk in chunks]
    embeddings = embedding_service.generate_embeddings_batch(texts)
    
    # Store in vector DB
    vector_store.upsert_chunks(chunks, embeddings)
    
    # Test query about Python
    query = "Tell me about Python programming"
    query_embedding = embedding_service.generate_embedding(query)
    results = vector_store.similarity_search(query_embedding, top_k=1)
    
    # Should return Python chunk as most relevant
    assert len(results) > 0
    assert "Python" in results[0]['text']
    assert results[0]['similarity_score'] > 0.5  # Should be reasonably similar


def test_similarity_scores(embedding_service, vector_store):
    """Test that similarity scores are reasonable."""
    
    # Create test chunk
    chunk = DocumentChunk(
        chunk_id="test",
        text="The quick brown fox jumps over the lazy dog.",
        metadata=ChunkMetadata(source="test.txt", chunk_id="test")
    )
    
    embedding = embedding_service.generate_embedding(chunk.text)
    vector_store.upsert_chunks([chunk], [embedding])
    
    # Query with exact same text
    query_embedding = embedding_service.generate_embedding(chunk.text)
    results = vector_store.similarity_search(query_embedding, top_k=1)
    
    # Exact match should have very high similarity
    assert len(results) > 0
    assert results[0]['similarity_score'] > 0.95


def test_top_k_retrieval(embedding_service, vector_store):
    """Test that top_k parameter works correctly."""
    
    # Create multiple chunks
    chunks = [
        DocumentChunk(
            chunk_id=str(i),
            text=f"Document number {i} with some content.",
            metadata=ChunkMetadata(source=f"doc{i}.txt", chunk_id=str(i))
        )
        for i in range(10)
    ]
    
    texts = [chunk.text for chunk in chunks]
    embeddings = embedding_service.generate_embeddings_batch(texts)
    vector_store.upsert_chunks(chunks, embeddings)
    
    # Test different top_k values
    query_embedding = embedding_service.generate_embedding("document content")
    
    results_3 = vector_store.similarity_search(query_embedding, top_k=3)
    results_5 = vector_store.similarity_search(query_embedding, top_k=5)
    
    assert len(results_3) == 3
    assert len(results_5) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
