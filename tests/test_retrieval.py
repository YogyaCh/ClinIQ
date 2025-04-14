import pytest
from unittest.mock import patch, MagicMock
import os

# Patch Chroma, HuggingFaceEmbeddings, TextLoader, and CharacterTextSplitter
@patch("backend.vector.ingest_knowledgebase.os.listdir")
@patch("backend.vector.ingest_knowledgebase.TextLoader")
@patch("backend.vector.ingest_knowledgebase.CharacterTextSplitter")
@patch("backend.vector.ingest_knowledgebase.Chroma")
def test_ingest_knowledgebase_success(mock_chroma, mock_splitter, mock_loader, mock_listdir):
    # Mock file listing
    mock_listdir.return_value = ["doc1.txt", "doc2.txt"]

    # Mock TextLoader
    mock_loader_instance = MagicMock()
    mock_loader_instance.load.return_value = ["text1"]
    mock_loader.return_value = mock_loader_instance

    # Mock splitter
    mock_splitter_instance = MagicMock()
    mock_splitter_instance.split_documents.return_value = ["chunk1", "chunk2"]
    mock_splitter.return_value = mock_splitter_instance

    # Mock Chroma
    mock_chroma_instance = MagicMock()
    mock_chroma.return_value = mock_chroma_instance
    mock_chroma.from_documents.return_value = mock_chroma_instance

    from backend.retrieval import ingest_knowledgebase
    vectordb = ingest_knowledgebase()

    assert vectordb == mock_chroma_instance
    mock_chroma_instance.persist.assert_called_once()

@patch("backend.vector.ingest_knowledgebase.Chroma")
def test_get_contextual_knowledge_success(mock_chroma):
    mock_retriever = MagicMock()
    mock_retriever.get_relevant_documents.return_value = [MagicMock(page_content="Result 1"), MagicMock(page_content="Result 2")]

    mock_chroma_instance = MagicMock()
    mock_chroma_instance.as_retriever.return_value = mock_retriever
    mock_chroma.return_value = mock_chroma_instance

    from backend.retrieval import get_contextual_knowledge
    context = get_contextual_knowledge("anemia")

    assert "Result 1" in context
    assert "Result 2" in context

@patch("backend.ingest_knowledgebase.os.listdir", return_value=["badfile.txt"])
@patch("backend.ingest_knowledgebase.TextLoader")
def test_ingest_knowledgebase_loader_failure(mock_loader, mock_listdir):
    mock_loader_instance = mock_loader.return_value
    mock_loader_instance.load.side_effect = Exception("file read error")

    from backend.retrieval import ingest_knowledgebase
    with pytest.raises(Exception) as e:
        ingest_knowledgebase()
    assert "file read error" in str(e.value)

@patch("backend.ingest_knowledgebase.Chroma", side_effect=Exception("db load error"))
def test_get_contextual_knowledge_failure(mock_chroma):
    from backend.retrieval import get_contextual_knowledge
    with pytest.raises(Exception) as e:
        get_contextual_knowledge("query")
    assert "db load error" in str(e.value)
