from .models import RSSFeed

def get_rss_list(request):
    if request.user.is_anonymous:
        return {'user_rss_list': RSSFeed.objects.all()}
    else:
        return {'user_rss_list': request.user.profile.get_rss_list()}

def get_rss_articles(request):
    # TODO: Set default for user in model and get that here
    default_feed = RSSFeed.objects.get(name="Quanta Magazine")
    article_list = default_feed.get_popular_article_list()
    # article_list = []
    return {'default_article_list': article_list}
