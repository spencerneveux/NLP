import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NLP.settings')

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "C:/Users/spenc/PycharmProjects/NLP/NLP/app/api.json"
django.setup()

from NLP.app.static.python.nlp import NLP
from NLP.app.static.python.crawler import Crawler
# from NLP.app.static.python.nlp import NLP
# from NLP.app.static.python.crawler import Crawler
# from NLP.app.static.python.entity import Entity
# from NLP.app.static.python.sentiment import Sentiment
# from NLP.app.static.python.category import Category


if __name__ == '__main__':
    nlp = NLP()
    c = Crawler()
    c.process_feeds()
    feeds = c.get_feeds()
    for feed in feeds:
        articles = feed.get_articles()
        for article in articles:
            # Analyze article content
            nlp.analyze_entities(article.summary)
            nlp.analyze_categories(article.summary)
            nlp.analyze_sentiment(article.summary)
