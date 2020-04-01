from .models import RSSFeed

def get_rss_list(request):
    return {'rss_list': RSSFeed.objects.all()}

def get_rss_articles(request):
    # TODO: Set default for user in model and get that here
    default_feed = RSSFeed.objects.get(name="Quanta Magazine")
    article_list = default_feed.get_popular_article_list()
    return {'default_article_list': article_list}