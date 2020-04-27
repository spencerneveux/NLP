from .models import RSSFeed, RSS

def get_rss_list(request):
    if request.user.is_anonymous:
        return {'user_rss_list': RSSFeed.objects.all()[:10]}
    else:
        if request.user.profile.get_rss_list():
            return {'user_rss_list': request.user.profile.get_rss_list()}
        else:
            return {'user_rss_list': RSSFeed.objects.all()[:10]}

def get_rss_articles(request):
    # TODO: Set default for user in model and get that here
    if request.user.is_anonymous:
        default_feed = RSSFeed.objects.get(name="Xbox")
        article_list = default_feed.get_popular_article_list()

        return {'default_article_list': article_list}
    else:
        if request.user.profile.get_first_rss():
            default_feed = request.user.profile.get_first_rss()
            article_list = default_feed.get_popular_article_list()
        else:
            default_feed = RSSFeed.objects.get(name="Xbox")
            article_list = default_feed.get_popular_article_list()
        return {'default_article_list': article_list}
