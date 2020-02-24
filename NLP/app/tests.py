from django.test import TestCase
from models import Article


class ArticleTestCase(TestCase):
    def setup(self):
        Article.objects.create(author="Joe Schmo", publisher="Test Publisher", title="Test Title", content="lorem ipsum")

    def test_article(self):
        article = Article.objects.get(author="Joe Schmo")
        self.assertEqual(article.test_method(), "Test")

