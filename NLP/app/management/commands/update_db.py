import os
import requests

from django.core.management.base import BaseCommand, CommandError
from ...models import (
    RSSFeed,
    Article,
    Category,
    Entity,
    Score,
    Knowledge,
    MetaData
)

from ...static.python.nlp import NLP
from ...static.python.crawler import Crawler
# from ...static.python.category import Category
# from ...static.python.entity import Entity
# from ...static.python.knowledge import Knowledge
# from ...static.python.metadata import Metadata
# from ...static.python.score import Score

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "C:/Users/spenc/PycharmProjects/NLP/NLP/api.json"

class Command(BaseCommand):
    help = 'Testing RSSFeed'

    def add_arguments(self, parser):
        parser.add_argument('arg_list', nargs='+', type=str)

    def handle(self, *args, **options):
        for arg in options['arg_list']:
            if arg == "start":
                self.stdout.write(self.style.SUCCESS('Starting'))
                try:
                    nlp = NLP()
                    crawler = Crawler()
                    crawler.process_feeds()
                    feeds = crawler.get_feeds()

                    # Iterate over all feeds
                    for feed in feeds:
                        f_db, created = RSSFeed.objects.get_or_create(name=feed.get_title(), link=feed.get_link())

                        if created:
                            print(f"Created RSS Feed {f_db.pk}")
                        else:
                            print(f"Found RSS Feed {f_db.pk}")

                        # Get all articles from current feed.
                        articles = feed.get_articles()

                        # Iterate over each article
                        for article in articles:
                            # TODO: fix publisher
                            a_db, created = Article.objects.get_or_create(rss_feed=f_db, title=article.title, publisher="test Publisher", author=article.author, content=article.content, link=article.link)

                            # Analyze article content
                            self.stdout.write(self.style.SUCCESS('Analyzing article'))
                            if len(article.summary) > 100:
                                nlp.analyze_entities(article.summary)
                                self.stdout.write(self.style.SUCCESS('Entities Complete'))

                                nlp.analyze_categories(article.summary)
                                self.stdout.write(self.style.SUCCESS('Categories Complete'))

                                nlp.analyze_sentiment(article.summary)
                                self.stdout.write(self.style.SUCCESS('Sentiment Complete'))

                            # Retrieve results
                            entities = nlp.get_entities()
                            categories = nlp.get_categories()
                            metadata = nlp.get_metadata()
                            nlp.calculate_avg()
                            avg_score = nlp.get_avg_score()
                            avg_magnitude = nlp.get_avg_magnitude()

                            # Create categories for article
                            for category in categories.categories:
                                c_db = Category.objects.create(article=a_db, name=category.name, confidence=category.confidence)

                            for entity in entities.entities:
                                e_db = Entity.objects.create(article=a_db, name=entity.name, salience=entity.salience, entity_type=entity.type)

                                if entity.metadata:
                                    if entity.metadata.get(
                                            "wikipedia_url") and entity.metadata.get(
                                            "mid"):

                                        # Knowledge base api call/handling
                                        self.stdout.write(
                                            self.style.SUCCESS('Calling Knowledge API'))

                                        # TODO: Separate api key from file
                                        knowledge_results = requests.get(
                                            "https://kgsearch.googleapis.com/v1/entities:search?ids=" + entity.metadata.get(
                                                "mid") + "&key=AIzaSyBVWNLOTmBPy63hgF2ZgSLuOsFqFVRWSoQ&limit=1&indent=True")
                                        json_results = knowledge_results.json().get(
                                            'itemListElement')

                                        try:
                                            results = json_results[0]['result']

                                            # Get values from request
                                            name = results.get('name')
                                            desc = results.get('description')
                                            image_details = results.get('image')
                                            desc_details = results.get(
                                                'detailedDescription')
                                            url_details = results.get('url')

                                            key = entity.metadata.get(
                                                "wikipedia_url")
                                            value = entity.metadata.get("mid")

                                            if (image_details):
                                                image_content_url = \
                                                image_details['contentUrl']
                                                image_url = image_details['url']

                                            # Get Detailed Description
                                            if (desc_details):
                                                article_body = desc_details[
                                                    'articleBody']
                                                article_url = desc_details[
                                                    'url']

                                            # Create knowledge object
                                            k_db = Knowledge.objects.create(
                                                entity=e_db, name=name,
                                                description=desc,
                                                url=article_url,
                                                article_body=article_body)

                                            # Create Metadata Object
                                            m_db = MetaData.objects.create(
                                                entity=e_db, key=key,
                                                value=value)

                                        except:
                                            print("No Results from Knowledge Call")

                        # Create score object
                        s_db, created = Score.objects.get_or_create(article=a_db, magnitude=avg_magnitude, score=avg_score)

                except RSSFeed.DoesNotExist:
                    raise CommandError('Command "%s" experienced an error' % arg)


                self.stdout.write(self.style.SUCCESS('Successfully ran "%s"' % arg))