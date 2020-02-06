from google.cloud import language_v1
from google.cloud.language_v1 import enums


class NLP:
    def __init__(self):
        self.entity_dict = {}
        self.sentiment_dict = {}

        self.language = "en"

        self.avg_score = 0
        self.avg_magnitude = 0

        self.names = []
        self.metadata = []
        self.magnitudes = []
        self.entity_types = []
        self.salience_list = []
        self.sentiment_list = []
        self.sentiment_scores = []

        self.type = enums.Document.Type.PLAIN_TEXT
        self.encoding_type = enums.EncodingType.UTF8

        self.score_dict = {
            # Score Result : {'score', 'magnitude'}
            "clearly positive": [0.8, 3.0],
            "clearly negative": [-0.6, 4.0],
            "neutral": [0.1, 0.0],
            "mixed": [0.0, 4.0],
        }

    # =========================
    # Getters
    # =========================
    def get_entities(self):
        return self.entity_dict

    def get_metadata(self):
        return self.metadata

    def get_names(self):
        return self.names

    def get_types(self):
        return self.entity_types

    def get_salience(self):
        return self.salience_list

    def get_sentiment(self):
        return self.sentiment_dict

    def get_magnitudes(self):
        return self.magnitudes

    def get_scores(self):
        return self.sentiment_scores

    def get_sentiment_list(self):
        return self.sentiment_list

    def get_avg_magnitude(self):
        return self.avg_magnitude

    def get_avg_score(self):
        return self.avg_score

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
            self.names.append(entity.name)

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

    def analyze_avg(self):
        for score in self.score_dict.items():

            if (
                self.avg_magnitude >= score[1][0]
                and self.avg_score >= score[1][1]
            ):
                print(score[0])


# =========================
# Testing
# =========================
def main():
    nlp = NLP()
    text = "In a pair of votes whose outcome was never in doubt, the Senate fell well short of the two-thirds margin that would have been needed to remove Mr. Trump, formally concluding the three-week-long trial of the 45th president that has roiled Washington and threatened the presidency. The verdicts came down almost entirely upon party lines, with every Democrat voting “guilty” on both charges and Republicans uniformly voting “not guilty” on the obstruction of Congress charge."

    # Analyze
    nlp.analyze_entities(text)
    nlp.analyze_sentiment(text)

    # Report Results
    # print(nlp.get_metadata())
    # print(nlp.get_names())
    # print(nlp.get_types())
    # print(nlp.get_salience())
    # print(nlp.get_sentiment())
    # print(f"Magnitude: {nlp.get_magnitudes()}")
    # print(f"Scores: {nlp.get_scores()}")
    # print(nlp.get_sentiment_list())
    nlp.calculate_avg()
    nlp.analyze_avg()


if __name__ == "__main__":
    main()
