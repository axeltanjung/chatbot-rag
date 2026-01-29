"""Vector store abstraction layer using ChromaDB."""

from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from config import settings
from models import DocumentChunk


class VectorStore:
    """Vector database interface using ChromaDB."""
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        # Initialize persistent client
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=settings.anonymized_telemetry
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
    
    def upsert_chunks(self, chunks: List[DocumentChunk], embeddings: List[List[float]]):
        """
        Insert or update document chunks with their embeddings.
        
        Args:
            chunks: List of document chunks
            embeddings: Corresponding embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")
        
        # Prepare data for ChromaDB
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [
            {
                'source': chunk.metadata.source,
                'page': chunk.metadata.page if chunk.metadata.page else -1,
                'created_at': chunk.metadata.created_at.isoformat()
            }
            for chunk in chunks
        ]
        
        # Upsert to collection
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
    
    def similarity_search(
        self, 
        query_embedding: List[float], 
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar chunks using cosine similarity.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of results with text, metadata, and similarity scores
        """
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                result = {
                    'chunk_id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_documents(self) -> List[Dict]:
        """
        Get list of all indexed documents.
        
        Returns:
            List of document information
        """
        # Get all items from collection
        all_items = self.collection.get()
        
        # Group by source
        documents = {}
        for i, metadata in enumerate(all_items['metadatas']):
            source = metadata.get('source', 'Unknown')
            if source not in documents:
                documents[source] = {
                    'filename': source,
                    'num_chunks': 0,
                    'chunk_ids': []
                }
            documents[source]['num_chunks'] += 1
            documents[source]['chunk_ids'].append(all_items['ids'][i])
        
        return list(documents.values())
    
    def delete_document(self, filename: str) -> int:
        """
        Delete all chunks from a specific document.
        
        Args:
            filename: Name of the document to delete
            
        Returns:
            Number of chunks deleted
        """
        # Get all chunks for this document
        results = self.collection.get(
            where={"source": filename}
        )
        
        if results['ids']:
            # Delete chunks
            self.collection.delete(ids=results['ids'])
            return len(results['ids'])
        
        return 0
    
    def get_collection_info(self) -> Dict:
        """Get information about the vector store."""
        count = self.collection.count()
        return {
            'collection_name': settings.chroma_collection_name,
            'total_chunks': count,
            'persist_directory': settings.chroma_persist_directory,
            'similarity_metric': 'cosine'
        }
    
    def clear_collection(self):
        """Delete all data from the collection."""
        # Delete and recreate collection
        self.client.delete_collection(name=settings.chroma_collection_name)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"}
        )
