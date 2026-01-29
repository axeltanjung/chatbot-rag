from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChunkMetadata(BaseModel):
    """Metadata for a document chunk."""
    source: str
    page: Optional[int] = None
    chunk_id: str
    created_at: datetime = Field(default_factory=datetime.now)


class DocumentChunk(BaseModel):
    """Represents a chunk of a document."""
    chunk_id: str
    text: str
    metadata: ChunkMetadata


class DocumentUploadResponse(BaseModel):
    """Response after uploading a document."""
    document_id: str
    filename: str
    num_chunks: int
    message: str


class DocumentInfo(BaseModel):
    """Information about an indexed document."""
    document_id: str
    filename: str
    num_chunks: int
    created_at: datetime


class Source(BaseModel):
    """Source citation for a chat response."""
    chunk_id: str
    text: str
    source: str
    page: Optional[int] = None
    similarity_score: float


class ChatRequest(BaseModel):
    """Request for chat endpoint."""
    query: str
    chat_history: List[dict] = Field(default_factory=list)
    top_k: int = 5


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    answer: str
    sources: List[Source]
    confidence: float
    prompt_used: Optional[str] = None  # For developer mode


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
