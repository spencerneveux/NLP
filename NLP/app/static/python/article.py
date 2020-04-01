from .entity import Entity
from .category import Category
from .sentiment import Sentiment
from .score import Score

class Article:
    def __init__(self):
        self.title: str = ""
        self.author: str = ""
        self.publisher: str = ""
        self.link: str = ""
        self.published: str = ""
        self.summary: str = ""
        self.content: str = ""
        self.score: Score
        self.entities: [Entity] = []
        self.categories: [Category] = []
        self.sentiment: [Sentiment] = []

    # =========================
    # Getters
    # =========================
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_publisher(self):
        return self.publisher

    def get_content(self):
        return self.content

    def get_link(self):
        return self.link

    def get_published(self):
        return self.published

    def get_summary(self):
        return self.summary

    def get_score(self):
        return self.score

    def get_entities(self):
        return self.entities

    def get_sentiment(self):
        return self.sentiment

    def get_categories(self):
        return self.categories

    # =========================
    # Setters
    # =========================
    def set_title(self, title:str):
        self.title = title

    def set_author(self, author:str):
        self.author = author

    def set_publisher(self, publisher:str):
        self.publisher = publisher

    def set_content(self, content:str):
        self.content = content

    def set_link(self, link:str):
        self.link = link

    def set_published(self, published:str):
        self.published = published

    def set_summary(self, summary:str):
        self.summary = summary

    def set_score(self, score:Score):
        self.score = score

    def set_entities(self, entity:Entity):
        self.entities.append(entity)

    def set_categories(self, category:Category):
        self.categories.append(category)

    def set_sentiment(self, sentiment:Sentiment):
        self.categories.append(sentiment)

    def __str__(self):
        return f"{self.title} - {self.entities} - {self.categories}"