from .article import Article

class Feed:
    def __init__(self):
        self.title: str = ""
        self.link: str = ""
        self.description: str = ""
        self.published_date: str = ""
        self.articles = []

    # =========================
    # Getters
    # =========================
    def get_title(self):
        return self.title

    def get_link(self):
        return self.link

    def get_description(self):
        return self.description

    def get_published_date(self):
        return self.published_date

    def get_articles(self):
        return self.articles

    # =========================
    # Setters
    # =========================
    def set_title(self, title:str):
        self.title = title

    def set_link(self, link:str):
        self.link = link

    def set_description(self, desc:str):
        self.description = desc

    def set_published_date(self, date:str):
        self.published_date = date

    def set_articles(self, article:Article):
        self.articles.append(article)

    def __str__(self):
        return self.title + " - " + self.link