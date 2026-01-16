
import sys
from unittest.mock import MagicMock, patch
import pytest

# Mock NER results data
MOCK_NER_RESULTS = [
    {"entity": "B-PERSON", "score": 0.99, "index": 1, "word": "Nguyễn", "start": 0, "end": 6},
    {"entity": "I-PERSON", "score": 0.98, "index": 2, "word": "Văn", "start": 7, "end": 10},
    {"entity": "I-PERSON", "score": 0.97, "index": 3, "word": "A", "start": 11, "end": 12},
    {"entity": "B-ORGANIZATION", "score": 0.80, "index": 4, "word": "Công", "start": 15, "end": 19}, # low score, might be filtered
    {"entity": "I-ORGANIZATION", "score": 0.95, "index": 5, "word": "Ty", "start": 20, "end": 22},
]

@pytest.fixture(autouse=True)
def mock_transformers_module():
    """
    Mock transformers module globally for the tests in this file.
    This fixture runs before each test.
    """
    mock_transformers = MagicMock()

    # Setup nested mocks
    mock_transformers.logging = MagicMock()
    mock_transformers.AutoModelForTokenClassification = MagicMock()
    mock_transformers.AutoTokenizer = MagicMock()
    mock_transformers.pipeline = MagicMock()
    mock_transformers.models.electra.configuration_electra = MagicMock()

    # Patch sys.modules
    with patch.dict(sys.modules, {
        'transformers': mock_transformers,
        'transformers.models.electra.configuration_electra': MagicMock(),
    }):
        # Remove the module under test so it re-imports with our mocks
        if 'vnnews_graph_producer.entity_extractor' in sys.modules:
            del sys.modules['vnnews_graph_producer.entity_extractor']

        yield mock_transformers

def test_ner_calls_pipeline(mock_transformers_module):
    from vnnews_graph_producer import entity_extractor

    # Setup pipeline mock return value
    # Note: entity_extractor.nlp is already initialized at import time
    # which happened inside the fixture setup (implied by re-importing in test or previously)
    # Actually, we need to import inside the test to ensure we get the re-imported module
    # But wait, pytest fixture yields, so the patch is active.

    mock_nlp_instance = entity_extractor.nlp
    mock_nlp_instance.return_value = MOCK_NER_RESULTS

    # Test ner function
    text = "Nguyễn Văn A Công Ty"
    results = entity_extractor.ner(text, False, 0.9)

    # Verify pipeline was called with correct text
    mock_nlp_instance.assert_called_with(text)

    # Verify filtering logic works (score >= 0.9)
    assert len(results) == 4
    assert results[0]['word'] == "Nguyễn"

def test_pipeline_initialization_once(mock_transformers_module):
    # Reset mocks
    mock_transformers_module.pipeline.reset_mock()

    # Reload module to trigger initialization
    if 'vnnews_graph_producer.entity_extractor' in sys.modules:
        del sys.modules['vnnews_graph_producer.entity_extractor']

    from vnnews_graph_producer import entity_extractor

    # Setup the mock nlp object to return a list
    entity_extractor.nlp.return_value = []

    # Verify pipeline was initialized once (at import time)
    mock_transformers_module.pipeline.assert_called_once()

    # Call ner multiple times
    entity_extractor.ner("text 1", False, 0.5)
    entity_extractor.ner("text 2", False, 0.5)

    # Verify pipeline was NOT initialized again (call count should still be 1)
    assert mock_transformers_module.pipeline.call_count == 1
