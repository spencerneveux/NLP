class Sentiment:
    def __init__(self):
        self.document_sentiment: dict = {}

    def get_document_sentiment(self):
        return self.document_sentiment

    def set_document_sentiment(self, sentiment: dict):
        self.document_sentiment['magnitude'] = sentiment['magnitude']
        self.document_sentiment['score'] = sentiment['score']
