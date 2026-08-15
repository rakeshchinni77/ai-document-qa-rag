import pytest
from backend.app.services.prompt_service import PromptService

def test_prompt_builder_includes_all_retrieved_chunks():
    chunks = [
        "Chunk 1: NovaTech reported Q3 revenue of $42.5 million.",
        "Chunk 2: Gross profit margin expanded to 74.2%.",
        "Chunk 3: Customer retention rates remained high at 96.4%."
    ]
    question = "What was NovaTech's Q3 revenue?"
    
    prompt = PromptService.build_prompt(question, chunks)
    
    # 1. Check user question appears in prompt
    assert question in prompt
    
    # 2. Check all retrieved chunks appear in prompt
    for chunk in chunks:
        assert chunk in prompt
        
    # 3. Check grounding rules & fallback statement exist in prompt
    assert "Rely ONLY on the provided context information" in prompt
    assert "Under no circumstances should you use outside knowledge or hallucinate." in prompt
    assert 'I cannot find the answer in the provided documents.' in prompt

def test_prompt_builder_single_chunk():
    chunks = ["Single retrieved chunk text content."]
    question = "Is this single chunk test?"
    
    prompt = PromptService.build_prompt(question, chunks)
    
    assert "Single retrieved chunk text content." in prompt
    assert "Is this single chunk test?" in prompt
    assert "--- Context Chunk 1 ---" in prompt
