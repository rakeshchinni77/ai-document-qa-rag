import pytest
from backend.app.services.llm_service import LLMService
from backend.app.core.exceptions import DownstreamLLMError

def test_real_groq_api_call():
    service = LLMService()
    prompt = """You are an expert AI assistant.
Context Information:
NovaTech reported total revenue of $42.5 million in Q3 2026.

Question: What was NovaTech Q3 revenue?
Answer:"""
    
    answer = service.generate_answer(prompt)
    assert answer is not None
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "42.5 million" in answer or "revenue" in answer.lower()

def test_invalid_groq_api_key_negative_test(monkeypatch):
    # Temporarily set invalid API key to test exception handling
    service = LLMService()
    service.groq_api_key = "gsk_invalid_test_key_xyz_999"
    
    with pytest.raises(DownstreamLLMError) as exc_info:
        service.generate_answer("Test question prompt?")
    
    assert exc_info.value.status_code == 502
    assert "LLM service communication failure" in exc_info.value.detail or "HTTP 401" in exc_info.value.detail
