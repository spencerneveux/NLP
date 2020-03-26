import os

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "C:/Users/spenc/PycharmProjects/NLP/NLP/app/api.json"


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

            # Retrieve results
            entities = nlp.get_entities()
            categories = nlp.get_categories()
            metadata = nlp.get_metadata()
            nlp.calculate_avg()
            avg_score = nlp.get_avg_score()
            avg_magnitude = nlp.get_avg_magnitude()

            for category in categories.categories:
                print(category)

            # # Create Category Models
            # for category in categories.categories:
            #     Category.objects.create(
            #         article_id=article.pk,
            #         name=category.name,
            #         confidence=category.confidence,
            #     )
            #
            # # Create Entity Models
            # for entity in entities.entities:
            #     e = Entity.objects.create(
            #         article_id=article.pk,
            #         name=entity.name,
            #         salience=round(entity.salience, 3),
            #         entity_type=enums.Entity.Type(entity.type).name,
            #     )
            #
            #     if entity.metadata:
            #         if entity.metadata.get(
            #                 "wikipedia_url") and entity.metadata.get("mid"):
            #
            #             # Knowledge base api call/handling
            #             knowledge_results = requests.get(
            #                 "https://kgsearch.googleapis.com/v1/entities:search?ids=" + entity.metadata.get(
            #                     "mid") + "&key=AIzaSyBVWNLOTmBPy63hgF2ZgSLuOsFqFVRWSoQ&limit=1&indent=True")
            #             json_results = knowledge_results.json().get(
            #                 'itemListElement')
            #             results = json_results[0]['result']
            #
            #             # Get values from request
            #             name = results.get('name')
            #             desc = results.get('description')
            #             image_details = results.get('image')
            #             desc_details = results.get('detailedDescription')
            #             url_details = results.get('url')
            #
            #             if (image_details):
            #                 image_content_url = image_details['contentUrl']
            #                 image_url = image_details['url']
            #
            #             # Get Detailed Description
            #             if (desc_details):
            #                 article_body = desc_details['articleBody']
            #                 article_url = desc_details['url']
            #
            #             # Create Knowledge Model
            #             Knowledge.objects.create(
            #                 entity_id=e.id,
            #                 name=name,
            #                 description=desc,
            #                 url=article_url,
            #                 article_body=article_body
            #             )
            #
            #             MetaData.objects.create(
            #                 entity_id=e.id,
            #                 key=entity.metadata.get("wikipedia_url"),
            #                 value=entity.metadata.get("mid"),
            #             )
            #         else:
            #             MetaData.objects.create(entity_id=e.id, key="",
            #                                     value="")
            #
            # # Create Score Model
            # Score.objects.create(
            #     article_id=article.pk, score=avg_score, magnitude=avg_magnitude
            # )
