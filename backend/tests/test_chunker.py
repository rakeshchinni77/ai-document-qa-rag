import pytest
from backend.app.services.chunker import TextChunker

def test_chunker_empty_text():
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    assert chunker.split_text("") == []
    assert chunker.split_text("   \n\t  ") == []

def test_chunker_short_text():
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    text = "Short text under 1000 characters."
    chunks = chunker.split_text(text)
    assert len(chunks) == 1
    assert chunks[0] == text

def test_chunker_exactly_1000_chars():
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    text = "A" * 1000
    chunks = chunker.split_text(text)
    assert len(chunks) == 1
    assert len(chunks[0]) == 1000

def test_chunker_over_1000_chars():
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    text = "A" * 2500
    chunks = chunker.split_text(text)
    # step size = 1000 - 200 = 800
    # chunk 1: 0..1000
    # chunk 2: 800..1800
    # chunk 3: 1600..2500 (length 900)
    assert len(chunks) == 3

def test_chunker_overlap_correctness():
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    # 0..100 -> step 80
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" * 10
    chunks = chunker.split_text(text)
    assert len(chunks) > 1
    # Check overlap: end of chunk 0 (last 20 chars) should match start of chunk 1 (first 20 chars)
    overlap_end = chunks[0][-20:]
    overlap_start = chunks[1][:20]
    assert overlap_end == overlap_start

def test_chunker_invalid_overlap():
    with pytest.raises(ValueError):
        TextChunker(chunk_size=100, chunk_overlap=100)

    with pytest.raises(ValueError):
        TextChunker(chunk_size=100, chunk_overlap=150)
