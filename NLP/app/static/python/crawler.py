import feedparser
from NLP.app.static.python.feed import Feed
from NLP.app.static.python.article import Article

rss_feeds = ['http://feeds.bbci.co.uk/news/world/rss.xml',
             'http://feeds.reuters.com/Reuters/worldNews',
             'http://feeds.washingtonpost.com/rss/rss_blogpost',
             'https://www.yahoo.com/news/rss/world',
             'http://rss.cnn.com/rss/edition_world.rss',
             'http://rssfeeds.usatoday.com/usatoday-newstopstories&x=1',
             'https://www.yahoo.com/news/rss/',
             'http://feeds.reuters.com/Reuters/domesticNews',
             'http://feeds.skynews.com/feeds/rss/us.xml',
             'http://rss.cnn.com/rss/edition_us.rss',
             'http://feeds.skynews.com/feeds/rss/uk.xml',
             'http://feeds.bbci.co.uk/news/rss.xml',
             'http://feeds.reuters.com/reuters/UKdomesticNews',
             'https://www.theguardian.com/uk/rss',
             'https://techcrunch.com/rssfeeds/',
             'http://rss.slashdot.org/Slashdot/slashdot',
             "https://news.google.com/news/rss",
             'https://spectrum.ieee.org/rss/blog/tech-talk/fulltext',
             'https://www.techworld.com/news/rss',
             'https://www.wired.com/feed',
             'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
             'https://www.npr.org/rss/rss.php?id=1045',
             'https://www.fandango.com/rss/newmovies.rss',
             'http://www.metacritic.com/rss/movies',
             'https://www.rogerebert.com/feed',
             'http://www.movies.com/rss-feeds/movie-news-rss',
             'http://www.si.com/rss/si_topstories.rss',
             'http://feeds1.nytimes.com/nyt/rss/Sports',
             'https://talksport.com/rss/sports-news/all/feed',
             'http://feeds.sport24.co.za/articles/Sport/Featured/TopStories/rss',
             'http://rss.cnn.com/rss/edition_sport.rss',
             'http://syndication.eonline.com/syndication/feeds/rssfeeds/topstories.xml',
             'http://feeds.reuters.com/reuters/entertainment',
             'http://www.instyle.com/feeds/all/ins.rss',
             'http://feeds.accesshollywood.com/AccessHollywood/LatestNews',
             'https://www.npr.org/rss/rss.php?id=1008',
             'https://api.quantamagazine.org/feed/']



class Crawler:
    def __init__(self):
        self.feed_list = [
            'https://api.quantamagazine.org/feed/'
        ]
        self.entries = []
        self.feeds = []
        self.update()

    def get_feeds(self):
        return self.feeds

    def set_feeds(self):
        for entry in self.entries:
            f = Feed()
            f.set_title(entry.feed.title)
            f.set_link(entry.feed.link)
            f.set_description(entry.feed.description)

            for article in entry.entries:
                a = Article()
                a.set_title(article.title)
                a.set_link(article.link)
                a.set_published(article.published)
                a.set_summary(article.summary)
                f.set_articles(a)
            self.feeds.append(f)

    def process_feeds(self):
        for feed in self.feed_list:
            self.entries.append(feedparser.parse(feed))

    def update(self):
        self.process_feeds()
        self.set_feeds()

    def __str__(self):
        return self.entries