import feedparser
import datetime
from urllib.parse import urlparse

from .feed import Feed
from .article import Article
# #
# from NLP.app.static.python.feed import Feed
# from NLP.app.static.python.article import Article

news_feeds = {
    "BBCI: News": 'http://feeds.bbci.co.uk/news/world/rss.xml',
    "NY Times: News": 'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml',
    "Buzzfeed: News": 'https://www.buzzfeed.com/world.xml',
    "Aljazeera": 'https://www.aljazeera.com/xml/rss/all.xml',
    "Global Issues": 'https://www.globalissues.org/news/feed',
    "The Cipher Brief": 'https://www.thecipherbrief.com/feed',
    "Yahoo: News": 'https://www.yahoo.com/news/rss/world',
    "CNN": 'http://rss.cnn.com/rss/edition_world.rss',
    "The Guardian: World News": 'https://www.theguardian.com/world/rss',
    "Washington Post": 'http://feeds.washingtonpost.com/rss/world',
    "CNBC": 'https://www.cnbc.com/id/100727362/device/rss/rss.html',
    "Reuters: World News": 'http://feeds.reuters.com/Reuters/worldNews',
    "NPR": 'https://feeds.npr.org/1004/rss.xml',
    "Sputnik News": 'https://sputniknews.com/export/rss2/world/index.xml',
    "Vox": 'https://www.vox.com/rss/world/index.xml',
    "Time": 'https://time.com/feed/',
    "ABC: News": 'https://abcnews.go.com/abcnews/internationalheadlines',
    "LA Times: World News": 'https://www.latimes.com/world/rss2.0.xml',
}

sport_feeds = {
    "Sporting News": 'http://www.sportingnews.com/us/rss',
    "Sky Sports": 'https://www.skysports.com/rss/12040',
    "Sports Keeda":'https://www.sportskeeda.com/feed',
    "Deadspin": 'https://deadspin.com/rss',
    "Reddit: Sports": 'https://www.reddit.com/r/sports/.rss?format=xml',
    "Inquirer: Sports": 'http://sports.inquirer.net/feed',
    "Sports on Earth": 'http://www.sportsonearth.com/gen/hb/rss/writers.xml',
    "Rivals": 'https://n.rivals.com/feed',
    "Sports Net": 'https://www.sportsnet.ca/feed/',
    "Essentially Sports": 'https://www.essentiallysports.com/feed/',
    "Sports Crunch": 'https://www.sportscrunch.in/feed/'
}

tech_feeds = {
    "Techmeme": 'https://www.techmeme.com/feed.xml?x=1',
    "Technology Review": 'https://www.technologyreview.com/feed/',
    "Arstechnica": 'http://feeds.arstechnica.com/arstechnica/technology-lab',
    "Vox": 'https://www.vox.com/rss/recode/index.xml',
    "Vergecast": 'https://feeds.megaphone.fm/vergecast',
    "Wired": 'https://www.wired.com/feed/rss',
    "Free Tech 4 Teachers": 'http://feeds.feedblitz.com/freetech4teachers',
    "BBC: Tech": 'http://feeds.bbci.co.uk/news/technology/rss.xml',
    "NY Times: Tech": 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
    "Medium: Starship Tech": 'https://medium.com/feed/starshiptechnologies',
    "CNET": 'https://www.cnet.com/rss/news/',
    "Reuters: Tech News": 'http://feeds.reuters.com/reuters/technologyNews',
    "The Verge": 'https://www.theverge.com/rss/frontpage',
    "Huff Post: Tech": 'https://www.huffpost.com/section/technology/feed',
    "ABC News: Tech": 'https://abcnews.go.com/abcnews/technologyheadlines',
    "The Atlantic": 'https://www.theatlantic.com/feed/channel/technology/',
    "Mirror": 'https://www.mirror.co.uk/tech/?service=rss'
}

business_feeds = {
    "CNBC": 'http://www.cnbc.com/id/19746125/device/rss/rss.xml',
    "Fortune": 'https://fortune.com/feed',
    "Investing": 'https://www.investing.com/rss/news.rss',
    "Seeking Alpha": 'https://seekingalpha.com/market_currents.xml',
    "Economic Times: India": 'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
    "Reuters: Business": 'http://feeds.reuters.com/reuters/INtopNews',
    "Yahoo: Finance": 'https://finance.yahoo.com/news/rssindex',
    "Business Standar": 'https://www.business-standard.com/rss/home_page_top_stories.rss',
}

political_feeds = {
    "Daily KOS": 'https://www.dailykos.com/blogs/main.rss',
    "NY Times: Politics": 'https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
    "Reddit: Politics": 'https://www.reddit.com/r/politics/.rss',
    "Politic USA": 'http://www.politicususa.com/feed',
    "News Busters": 'https://www.newsbusters.org/blog/feed',
    "The Gateway Pundit": 'https://www.thegatewaypundit.com/feed/',
    "The Political Insider": 'https://thepoliticalinsider.com/feed/',
    "The Guardian": 'https://www.theguardian.com/politics/blog/rss',
    "Huff Post: Politics": 'https://www.huffpost.com/section/politics/feed',
    "LA Times: Politics": 'https://www.latimes.com/politics/rss2.0.xml'
}

gaming_feeds = {
    "IGN": 'http://feeds.ign.com/ign/games-all',
    "Xbox": 'https://news.xbox.com/en-us/feed/',
    "Nintendo": 'http://www.nintendolife.com/feeds/latest',
    "Reddit: Gamers": 'https://www.reddit.com/r/gamers/.rss',
    "Polygon": 'https://www.polygon.com/rss/index.xml',
    "Euro Gamer": 'https://www.eurogamer.net/?format=rss',
    "Playstation": 'https://blog.us.playstation.com/feed/',
    "PC Gamer": 'https://www.pcgamer.com/rss/',
}

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
        self.feed_list = {
            'Quanta Magazine': 'https://api.quantamagazine.org/feed/',
            'Metacritic': 'http://www.metacritic.com/rss/movies',
            'Techworld': 'https://www.techworld.com/news/rss',
            'Wired': 'https://www.wired.com/feed',
            'Yahoo': 'https://www.yahoo.com/news/rss/',
            'RogerEbert': "https://www.rogerebert.com/feed",
            'Joe Rogan Podcasts': "http://podcasts.joerogan.net/feed",
            'Reddit':  "https://www.reddit.com/.rss",
        }

        self.entries = []
        self.feeds = []
        self.update()

    def get_feeds(self):
        return self.feeds

    def set_feeds(self):
        for entry in self.entries:
            print(entry)
            f = Feed()
            feed_keys = entry[2].feed.keys()

            f.set_category(entry[1])

            if 'title' in feed_keys:
                f.set_title(entry[0])

            if 'link' in feed_keys:
                link = entry[2].feed.link
                o = urlparse(link)
                netloc = o.netloc
                print(netloc)
                f.set_link(netloc)

            if 'description' in feed_keys:
                f.set_description(entry[2].feed.description)
            elif 'subtitle' in feed_keys:
                f.set_description(entry[2].feed.subtitle)
            elif 'subtitle_detail' in feed_keys:
                f.set_description(entry[2].feed.subtitle_detail['value'])

            print(f"Feed keys {feed_keys}")


            for article in entry[2].entries:
                a = Article()
                article_keys = article.keys()

                a.set_publisher(entry[0])

                if "title" in article_keys:
                    a.set_title(article.title)

                if "author" in article_keys:
                    a.set_author(article.author)

                if "link" in article_keys:
                    a.set_link(article.link)

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
        for feed in gaming_feeds:
            f = feedparser.parse(gaming_feeds[feed])
            if f.bozo == 0:
                tup = (feed, "Gaming", f)
                self.entries.append(tup)

        for feed in news_feeds:
            f = feedparser.parse(news_feeds[feed])
            if f.bozo == 0:
                tup = (feed, "News", f)
                self.entries.append(tup)

        for feed in tech_feeds:
            f = feedparser.parse(tech_feeds[feed])
            if f.bozo == 0:
                tup = (feed, "Tech", f)
                self.entries.append(tup)

        for feed in political_feeds:
            f = feedparser.parse(political_feeds[feed])
            if f.bozo == 0:
                tup = (feed, "Politics", f)
                self.entries.append(tup)

        for feed in business_feeds:
            f = feedparser.parse(business_feeds[feed])
            if f.bozo == 0:
                tup = (feed, "Business", f)
                self.entries.append(tup)

        for feed in sport_feeds:
            f = feedparser.parse(sport_feeds[feed])
            if f.bozo == 0:
                tup = (feed, "Sports", f)
                self.entries.append(tup)

    def update(self):
        self.process_feeds()
        self.set_feeds()

    def __str__(self):
        return self.entries

def main():
    c = Crawler()

main()