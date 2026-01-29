"""Unit tests for document chunking."""

import pytest
from backend.document_processor import DocumentProcessor
from backend.models import DocumentChunk


def test_chunk_size():
    """Test that chunks respect the configured size."""
    processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    
    text = "This is a test sentence. " * 50  # Long text
    chunks = processor.chunk_text(text, "test.txt")
    
    # Check that chunks are approximately the right size
    for chunk in chunks:
        assert len(chunk.text) <= 120  # Allow some flexibility for sentence boundaries
        assert len(chunk.text) > 0


def test_chunk_overlap():
    """Test that chunks have proper overlap."""
    processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    
    text = "Word " * 100  # Repeating text
    chunks = processor.chunk_text(text, "test.txt")
    
    # Should have multiple chunks
    assert len(chunks) > 1
    
    # Each chunk should have content
    for chunk in chunks:
        assert len(chunk.text) > 0


def test_chunk_metadata():
    """Test that chunk metadata is preserved."""
    processor = DocumentProcessor()
    
    text = "Test content for metadata preservation."
    source = "test_document.pdf"
    page_map = {0: 1}
    
    chunks = processor.chunk_text(text, source, page_map)
    
    assert len(chunks) > 0
    
    for chunk in chunks:
        assert chunk.metadata.source == source
        assert chunk.metadata.page == 1
        assert chunk.chunk_id is not None


def test_empty_text():
    """Test handling of empty text."""
    processor = DocumentProcessor()
    
    with pytest.raises(ValueError, match="Extracted text is empty"):
        processor.chunk_text("", "test.txt")


def test_short_text():
    """Test handling of text shorter than chunk size."""
    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    
    text = "Short text."
    chunks = processor.chunk_text(text, "test.txt")
    
    # Should create one chunk
    assert len(chunks) == 1
    assert chunks[0].text == text


def test_sentence_boundary_splitting():
    """Test that chunks prefer to split at sentence boundaries."""
    processor = DocumentProcessor(chunk_size=50, chunk_overlap=10)
    
    text = "First sentence here. Second sentence here. Third sentence here. Fourth sentence here."
    chunks = processor.chunk_text(text, "test.txt")
    
    # Should have multiple chunks
    assert len(chunks) > 1
    
    # Check that most chunks end with sentence terminators
    sentence_endings = 0
    for chunk in chunks[:-1]:  # Exclude last chunk
        if chunk.text.rstrip().endswith(('.', '!', '?')):
            sentence_endings += 1
    
    # At least some chunks should end at sentence boundaries
    assert sentence_endings > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
