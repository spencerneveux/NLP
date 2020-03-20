from .models import RSSFeed

def get_rss_list(request):
    return {'rss_list': RSSFeed.objects.all()}

def get_rss_articles(request):
    default_feed = RSSFeed.objects.get(pk=1)
    article_list = default_feed.get_article_list()
    return {'default_article_list': article_list}