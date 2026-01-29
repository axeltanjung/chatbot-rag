"""Document management API routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
from typing import List

from models import DocumentUploadResponse, DocumentInfo, ErrorResponse
from document_processor import DocumentProcessor
from embeddings import EmbeddingService
from vector_store import VectorStore

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize services
doc_processor = DocumentProcessor()
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Temporary upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document.
    
    - Validates file type
    - Extracts text
    - Chunks content
    - Generates embeddings
    - Stores in vector database
    """
    try:
        # Validate file type
        is_valid, error_msg = doc_processor.validate_file(file.filename)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Save uploaded file temporarily
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        temp_path = UPLOAD_DIR / f"{file_id}{file_extension}"
        
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        try:
            # Process document
            chunks, metadata = doc_processor.process_document(str(temp_path))
            
            # Generate embeddings
            chunk_texts = [chunk.text for chunk in chunks]
            embeddings = embedding_service.generate_embeddings_batch(chunk_texts)
            
            # Store in vector database
            vector_store.upsert_chunks(chunks, embeddings)
            
            return DocumentUploadResponse(
                document_id=file_id,
                filename=file.filename,
                num_chunks=len(chunks),
                message=f"Successfully indexed {len(chunks)} chunks from {file.filename}"
            )
        
        finally:
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/", response_model=List[DocumentInfo])
async def list_documents():
    """
    Get list of all indexed documents.
    """
    try:
        documents = vector_store.get_documents()
        
        # Convert to DocumentInfo format
        doc_infos = []
        for doc in documents:
            doc_infos.append(DocumentInfo(
                document_id=doc['chunk_ids'][0] if doc['chunk_ids'] else "unknown",
                filename=doc['filename'],
                num_chunks=doc['num_chunks'],
                created_at=None  # Would need to track this separately
            ))
        
        return doc_infos
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@router.delete("/{filename}")
async def delete_document(filename: str):
    """
    Delete a document and all its chunks from the vector store.
    """
    try:
        num_deleted = vector_store.delete_document(filename)
        
        if num_deleted == 0:
            raise HTTPException(status_code=404, detail=f"Document '{filename}' not found")
        
        return {
            "message": f"Deleted {num_deleted} chunks from '{filename}'",
            "num_chunks_deleted": num_deleted
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")


@router.get("/info")
async def get_vector_store_info():
    """
    Get information about the vector store.
    """
    try:
        info = vector_store.get_collection_info()
        embedding_info = embedding_service.get_embedding_info()
        
        return {
            **info,
            **embedding_info
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting info: {str(e)}")
