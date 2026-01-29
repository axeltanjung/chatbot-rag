"""Prompt templates for RAG system."""

SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based ONLY on the provided context.

STRICT RULES:
1. You MUST base your answer exclusively on the context provided below
2. If the context does not contain enough information to answer the question, respond with: "I don't have enough information in the provided documents to answer this question."
3. NEVER use outside knowledge or make assumptions beyond what's in the context
4. Always cite which source(s) you used to formulate your answer
5. Be concise but comprehensive
6. If you're uncertain, acknowledge it

Context:
{context}

Remember: Accuracy and honesty are more important than providing an answer."""


def build_rag_prompt(query: str, context_chunks: list[dict], chat_history: list[dict] = None) -> str:
    """
    Build the complete RAG prompt with context and query.
    
    Args:
        query: User's question
        context_chunks: List of retrieved chunks with metadata
        chat_history: Optional chat history for context
        
    Returns:
        Formatted prompt string
    """
    # Format context chunks
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        source = chunk.get('metadata', {}).get('source', 'Unknown')
        page = chunk.get('metadata', {}).get('page')
        text = chunk.get('text', '')
        
        page_info = f", Page {page}" if page else ""
        context_parts.append(f"[Source {i}: {source}{page_info}]\n{text}")
    
    context_str = "\n\n".join(context_parts)
    
    # Build messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context_str)}
    ]
    
    # Add chat history if provided
    if chat_history:
        messages.extend(chat_history)
    
    # Add current query
    messages.append({"role": "user", "content": query})
    
    return messages


def get_prompt_for_display(messages: list[dict]) -> str:
    """Convert messages to readable format for explainability."""
    parts = []
    for msg in messages:
        role = msg.get('role', 'unknown').upper()
        content = msg.get('content', '')
        parts.append(f"=== {role} ===\n{content}\n")
    return "\n".join(parts)
