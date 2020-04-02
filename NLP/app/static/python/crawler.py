import feedparser
import datetime
from .feed import Feed
from .article import Article
#
# from NLP.app.static.python.feed import Feed
# from NLP.app.static.python.article import Article

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
            # 'https://api.quantamagazine.org/feed/',
            # 'http://www.metacritic.com/rss/movies',
            # 'https://www.techworld.com/news/rss',
            # 'https://www.wired.com/feed',
            # 'https://www.yahoo.com/news/rss/',
            # "https://www.rogerebert.com/feed",
            # "http://podcasts.joerogan.net/feed",
            "https://www.reddit.com/.rss",
        ]
        self.entries = []
        self.feeds = []
        self.update()

    def get_feeds(self):
        return self.feeds

    def set_feeds(self):
        for entry in self.entries:
            print(entry)
            f = Feed()
            feed_keys = entry.feed.keys()

            # TODO: fix feed titles
            if 'title' in feed_keys:
                f.set_title(entry.feed.title)

            if 'link' in feed_keys:
                f.set_link(entry.feed.link)

            if 'description' in feed_keys:
                f.set_description(entry.feed.description)

            print(f"Feed keys {feed_keys}")


            for article in entry.entries:
                # print(article.keys())
                # print(article.values())
                #
                # print()

                a = Article()
                article_keys = article.keys()

                if "title" in article_keys:
                    a.set_title(article.title)

                if "author" in article_keys:
                    a.set_author(article.author)

                if "link" in article_keys:
                    a.set_link(article.link)

                # if "links" in article_keys:
                #     print(f"Links: {article.links}")

                if "summary" in article_keys:
                    a.set_summary(article.summary)

                if not "content" in article_keys:
                    if "summary_detail" in article_keys:
                        a.set_content(article.summary_detail['value'])

                elif "content" in article_keys:
                    a.set_content(article.content[0]['value'])

                f.set_articles(a)
            self.feeds.append(f)

    def process_feeds(self):
        for feed in self.feed_list:
            f = feedparser.parse(feed)
            if f.bozo == 0:
                self.entries.append(f)

    def update(self):
        self.process_feeds()
        self.set_feeds()

    def __str__(self):
        return self.entries

def main():
    c = Crawler()

main()