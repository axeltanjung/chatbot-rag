"""Chat API routes."""

from fastapi import APIRouter, HTTPException, Query

from models import ChatRequest, ChatResponse
from rag_engine import RAGEngine

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize RAG engine
rag_engine = RAGEngine()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    developer_mode: bool = Query(False, description="Include prompt in response for debugging")
):
    """
    Process a chat query using RAG.
    
    - Converts query to embedding
    - Retrieves relevant chunks
    - Generates grounded answer
    - Returns answer with sources and confidence
    """
    try:
        # Validate query
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query
        response = rag_engine.query(
            query=request.query,
            chat_history=request.chat_history,
            top_k=request.top_k,
            include_prompt=developer_mode
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "RAG Chat API"
    }
