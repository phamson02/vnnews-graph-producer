
import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock NER results data
MOCK_NER_RESULTS = [
    {"entity": "B-PERSON", "score": 0.99, "index": 1, "word": "Nguyễn", "start": 0, "end": 6},
    {"entity": "I-PERSON", "score": 0.98, "index": 2, "word": "Văn", "start": 7, "end": 10},
    {"entity": "I-PERSON", "score": 0.97, "index": 3, "word": "A", "start": 11, "end": 12},
    {"entity": "B-ORGANIZATION", "score": 0.80, "index": 4, "word": "Công", "start": 15, "end": 19}, # low score, might be filtered
    {"entity": "I-ORGANIZATION", "score": 0.95, "index": 5, "word": "Ty", "start": 20, "end": 22},
]

class TestEntityExtractor(unittest.TestCase):

    def setUp(self):
        # We need to mock transformers BEFORE importing the module under test
        self.mock_transformers = MagicMock()

        # Setup nested mocks
        self.mock_transformers.logging = MagicMock()
        self.mock_transformers.AutoModelForTokenClassification = MagicMock()
        self.mock_transformers.AutoTokenizer = MagicMock()
        self.mock_transformers.pipeline = MagicMock()
        self.mock_transformers.models.electra.configuration_electra = MagicMock()

        self.patcher = patch.dict(sys.modules, {
            'transformers': self.mock_transformers,
            'transformers.models.electra.configuration_electra': MagicMock(),
        })
        self.patcher.start()

        # Remove the module under test so it re-imports with our mocks
        if 'vnnews_graph_producer.entity_extractor' in sys.modules:
            del sys.modules['vnnews_graph_producer.entity_extractor']

    def tearDown(self):
        self.patcher.stop()

    def test_ner_calls_pipeline(self):
        from vnnews_graph_producer import entity_extractor

        # Setup pipeline mock return value
        mock_nlp_instance = entity_extractor.nlp
        mock_nlp_instance.return_value = MOCK_NER_RESULTS

        # Test ner function
        text = "Nguyễn Văn A Công Ty"
        results = entity_extractor.ner(text, False, 0.9)

        # Verify pipeline was called with correct text
        mock_nlp_instance.assert_called_with(text)

        # Verify filtering logic works (score >= 0.9)
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]['word'], "Nguyễn")

    def test_pipeline_initialization_once(self):
        # Reset mocks
        self.mock_transformers.pipeline.reset_mock()

        # Reload module to trigger initialization
        if 'vnnews_graph_producer.entity_extractor' in sys.modules:
            del sys.modules['vnnews_graph_producer.entity_extractor']

        from vnnews_graph_producer import entity_extractor

        # Setup the mock nlp object to return a list
        entity_extractor.nlp.return_value = []

        # Verify pipeline was initialized once (at import time)
        self.mock_transformers.pipeline.assert_called_once()

        # Call ner multiple times
        entity_extractor.ner("text 1", False, 0.5)
        entity_extractor.ner("text 2", False, 0.5)

        # Verify pipeline was NOT initialized again (call count should still be 1)
        self.assertEqual(self.mock_transformers.pipeline.call_count, 1)


if __name__ == '__main__':
    unittest.main()
