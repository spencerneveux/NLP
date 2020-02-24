import unittest
import os
# from .nlp import NLP 
from nlp import NLP

test_content = "Ringel’s conjecture predicts that certain kinds of complicated graphs — think Tinkertoy designs with trillions of pieces or more — can be “tiled,” or covered completely, by any individual copy of certain smaller graphs. Conceptually, the statement is like looking at a kitchen and asking: Can I completely cover the floor with identical copies of any type of tile in the store? In real life, most tiles won’t work for your particular kitchen — you’ll have to combine different shapes to cover the whole floor. But in the world of graph theory, the conjecture predicts that the tiling always works."

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/Users/spencerneveux/Desktop/FinalProject/NLP/NLP/app/api.json"


class NLPTest(unittest.TestCase):

    def test_entity_list(self):
        nlp = NLP()
        nlp.analyze_entities(test_content)
        self.assertTrue(nlp.get_entities_list())
        
    def test_entity_type(self):
        nlp = NLP()
        nlp.analyze_entities(test_content)
        self.assertTrue(nlp.get_entity_types())

    def test_entity_salience(self):
        nlp = NLP()
        nlp.analyze_entities(test_content)
        self.assertTrue(nlp.get_salience())

    def test_sentiment_dict(self):
        nlp = NLP()
        nlp.analyze_sentiment(test_content)
        self.assertTrue(nlp.get_sentiment())

    def test_sentiment_list(self):
        nlp = NLP()
        nlp.analyze_entities(test_content)
        self.assertTrue(nlp.get_sentiment_list())

    def test_sentiment_magnitude(self):
        nlp = NLP()
        nlp.analyze_entities(test_content)
        self.assertTrue(nlp.get_magnitudes())

    def test_sentiment_score(self):
        nlp = NLP()
        nlp.analyze_entities(test_content)
        self.assertTrue(nlp.get_scores())


if __name__ == '__main__':
    unittest.main()