import spacy
import numpy as np
import matplotlib.pyplot as plt
from google.cloud import language_v1
from google.cloud.language_v1 import enums


class NLP:
    def __init__(self):

        self.entity_dict = {}
        self.category_dict = {}
        self.sentiment_dict = {}

        self.language = "en"

        self.avg_score = 0
        self.avg_magnitude = 0

        self.metadata = []
        self.magnitudes = []
        self.entity_types = []
        self.entities_list = []
        self.salience_list = []
        self.sentiment_list = []
        self.categories_list = []
        self.confidence_list = []
        self.sentiment_scores = []

        self.type = enums.Document.Type.PLAIN_TEXT
        self.encoding_type = enums.EncodingType.UTF8

        self.score_dict = {
            # Score Result : {'score', 'magnitude'}
            "clearly positive": [0.8, 3.0],
            "neutral": [0.1, 0.0],
            "clearly negative": [-0.6, 4.0],
            "mixed": [0.0, 4.0],
        }

    # =========================
    # Getters
    # =========================
    def get_entities(self):
        return self.entity_dict

    def get_sentiment(self):
        return self.sentiment_dict

    def get_categories(self):
        return self.category_dict

    def get_metadata(self):
        return self.metadata

    def get_names(self):
        return self.names

    def get_entity_types(self):
        return self.entity_types

    def get_salience(self):
        return self.salience_list

    def get_magnitudes(self):
        return self.magnitudes

    def get_scores(self):
        return self.sentiment_scores

    def get_sentiment_list(self):
        return self.sentiment_list

    def get_entities_list(self):
        return self.entities_list

    def get_avg_magnitude(self):
        return self.avg_magnitude

    def get_avg_score(self):
        return self.avg_score

    def get_categories_list(self):
        return self.categories_list

    # =========================
    # Analysis
    # =========================
    def analyze_entities(self, text):
        client = language_v1.LanguageServiceClient()
        document = {
            "content": text,
            "type": self.type,
            "language": self.language,
        }
        self.entity_dict = client.analyze_entities(
            document, encoding_type=self.encoding_type
        )

        # Iterate over all entities
        for entity in self.entity_dict.entities:
            # Get all names
            self.entities_list.append(entity.name)

            # Get all types
            self.entity_types.append(enums.Entity.Type(entity.type).name)

            # Get all salience scores
            self.salience_list.append(entity.salience)

            # Get all metadata
            for metadata_value in entity.metadata.items():
                self.metadata.append(metadata_value)

    def analyze_sentiment(self, text):
        client = language_v1.LanguageServiceClient()
        document = {
            "content": text,
            "type": self.type,
            "language": self.language,
        }
        self.sentiment_dict = client.analyze_sentiment(
            document, encoding_type=self.encoding_type
        )

        for sentence in self.sentiment_dict.sentences:
            # Get sentiment
            self.sentiment_list.append(
                [sentence.sentiment.magnitude, sentence.sentiment.score]
            )

            # Get magnitudes
            self.magnitudes.append(sentence.sentiment.magnitude)
            # Get scores
            self.sentiment_scores.append(sentence.sentiment.score)

    def analyze_categories(self, text):
        client = language_v1.LanguageServiceClient()
        document = {
            "content": text,
            "type": self.type,
            "language": self.language,
        }
        self.category_dict = client.classify_text(document)

        for category in self.category_dict.categories:
            # Get category names
            self.categories_list.append(category.name)
            # Get confidence levels
            self.confidence_list.append(category.confidence)

    def calculate_avg(self):
        m_total = 0
        s_total = 0
        num_elems = len(self.sentiment_list)

        # Get total scores
        for score in self.sentiment_list:
            m_total += score[0]
            s_total += score[1]

        # Get average score
        self.avg_magnitude = m_total / num_elems
        self.avg_score = s_total / num_elems

        print(
            f"Total Magnitude: {m_total} -- Avg Magnitude: {self.avg_magnitude}"
        )
        print(f"Total Score: {s_total} -- Avg Score: {self.avg_score}")

    def check_clickbait(self, title):
        # This causes a massive performance hit
        nlp = spacy.load('en_core_web_md')
        tokens = nlp(title)

        max_salience = 0
        max_entity = ""
        for entity in self.entity_dict.entities:
            if (entity.salience > max_salience):
                max_salience = entity.salience
                max_entity = entity.name
                entity_token = nlp(max_entity)

        max_entity_dic = {max_entity, max_salience}

        for token in tokens:
            if (token.similarity(entity_token) > .3):
                print("Not Clickbait")
            else:
                print("Clickbait")


# =========================
# Testing
# =========================
def main():
    nlp = NLP()
    text = "In a pair of votes whose outcome was never in doubt, the Senate fell well short of the two-thirds margin that would have been needed to remove Mr. Trump, formally concluding the three-week-long trial of the 45th president that has roiled Washington and threatened the presidency. The verdicts came down almost entirely upon party lines, with every Democrat voting “guilty” on both charges and Republicans uniformly voting “not guilty” on the obstruction of Congress charge."

    # Analyze
    nlp.analyze_entities(text)
    nlp.analyze_sentiment(text)
    nlp.analyze_categories(text)
    nlp.analyze_avg()
    nlp.calculate_avg()

    # Report Results
    # print(nlp.get_metadata())
    # print(nlp.get_names())
    # print(nlp.get_types())
    # print(nlp.get_salience())
    # print(nlp.get_sentiment())
    # print(f"Magnitude: {nlp.get_magnitudes()}")
    # print(f"Scores: {nlp.get_scores()}")
    # print(nlp.get_sentiment_list())
    print(nlp.get_categories_list())

    # Graph
    nlp.graph()


if __name__ == "__main__":
    main()
