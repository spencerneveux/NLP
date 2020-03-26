import os
import requests

from django.core.management.base import BaseCommand, CommandError
from ...models import RSSFeed

from ...static.python.nlp import NLP
from ...static.python.crawler import Crawler
from ...static.python.category import Category
from ...static.python.entity import Entity
from ...static.python.knowledge import Knowledge
from ...static.python.metadata import Metadata
from ...static.python.score import Score

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
                        # Get all articles from current feed.
                        articles = feed.get_articles()

                        # Iterate over each article
                        for article in articles:

                            # Analyze article content
                            self.stdout.write(self.style.SUCCESS('Analyzing article'))
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
                                c = Category()
                                c.set_name(category.name)
                                c.set_confidence(category.confidence)
                                article.set_categories(c)

                            for entity in entities.entities:
                                e = Entity()
                                e.set_name(entity.name)
                                e.set_salience(entity.salience)
                                e.set_type(entity.type)

                                if entity.metadata:
                                    if entity.metadata.get(
                                            "wikipedia_url") and entity.metadata.get(
                                            "mid"):

                                        # Knowledge base api call/handling
                                        self.stdout.write(
                                            self.style.SUCCESS('Calling Knowledge API'))
                                        knowledge_results = requests.get(
                                            "https://kgsearch.googleapis.com/v1/entities:search?ids=" + entity.metadata.get(
                                                "mid") + "&key=AIzaSyBVWNLOTmBPy63hgF2ZgSLuOsFqFVRWSoQ&limit=1&indent=True")
                                        json_results = knowledge_results.json().get(
                                            'itemListElement')
                                        results = json_results[0]['result']

                                        # Get values from request
                                        name = results.get('name')
                                        desc = results.get('description')
                                        image_details = results.get('image')
                                        desc_details = results.get('detailedDescription')
                                        url_details = results.get('url')
                                        key = entity.metadata.get("wikipedia_url")
                                        value = entity.metadata.get("mid")

                                        if (image_details):
                                            image_content_url = image_details['contentUrl']
                                            image_url = image_details['url']

                                        # Get Detailed Description
                                        if (desc_details):
                                            article_body = desc_details['articleBody']
                                            article_url = desc_details['url']

                                        # Create knowledge object
                                        k = Knowledge()
                                        k.set_name(name)
                                        k.set_desc(desc)
                                        k.set_url(article_url)
                                        k.set_article_body(article_body)

                                        # Create Metadata Object
                                        m = Metadata()
                                        m.set_key(key)
                                        m.set_value(value)

                                        # Set entities knowledge/metadata
                                        e.set_knowledge(k)
                                        e.set_metadata(m)
                                    else:
                                        e.set_knowledge(Knowledge())
                                        e.set_metadata(Metadata())

                                # Set article entities
                                self.stdout.write(
                                    self.style.SUCCESS('Setting article entity'))
                                article.set_entities(e)

                            # Create score object
                            s = Score()
                            s.set_score(avg_score)
                            s.set_magnitude(avg_magnitude)
                            article.set_score(s)

                            print(f"Article Entities - {article.get_entities()}")

                except RSSFeed.DoesNotExist:
                    raise CommandError('Command "%s" experienced an error' % arg)


                self.stdout.write(self.style.SUCCESS('Successfully ran "%s"' % arg))