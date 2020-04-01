import os
import requests
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from google.cloud.language_v1 import enums
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .static.python.nlp import NLP


from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import (
    Author,
    Article,
    Publisher,
    Score,
    Entity,
    Category,
    MetaData,
    Knowledge,
    User,
    Profile,
    RSSFeed,
    Like,
    Comment,
    CommentForm,
    Favorite,
    Bookmark,
    RSS,
    SignUpForm,
    UpdateProfileForm,
)


# =========================
# Base Views
# =========================
class IndexView(TemplateView):
    template_name = "app/index.html"


class HomeView(ListView):
    model = Article
    template_name = "app/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rssfeed_list'] = RSSFeed.objects.all()
        return context

# =========================
# User
# =========================
class UserCreate(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


# =========================
# Account
# =========================
class AccountUpdate(UpdateView):
    model = User
    fields = ('email',)
    success_url = reverse_lazy("account")
    template_name = "app/account_form.html"

    def get_success_url(self):
        return reverse('account', kwargs={'pk': self.object.id})

# =========================
# Profile
# =========================
# TODO: fix all this nonsense
class ProfileCreate(CreateView):
    model = Profile
    fields = "__all__"


# =========================
# RSS Feeds
# =========================
class RSSList(ListView):
    model = RSSFeed

# =========================
# Comments
# =========================
class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = "app/comment_form.html"

    def form_valid(self, form):
        article = Article.objects.get(pk=self.kwargs['article_id'])
        form.instance.user = self.request.user
        form.instance.article = article
        return super(CommentCreateView, self).form_valid(form)


# =========================
# Articles
# =========================
class ArticleList(ListView):
    model = Article

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context

class ArticleScoreView(DetailView):
    model = Article
    template_name = "app/article_score.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["score_list"] = Score.objects.order_by("score")
        context["entity_list"] = Entity.objects.order_by("name")
        context["category_list"] = Category.objects.order_by("name")
        return context


class ArticleCreate(CreateView):
    model = Article
    fields = "__all__"

    def form_valid(self, form):
        # Save article to obtain pk
        article = form.save()

        # Instantiate nlp object to pass form content to nlp
        nlp = NLP()
        nlp.analyze_entities(form.instance.content)
        nlp.analyze_categories(form.instance.content)
        nlp.analyze_sentiment(form.instance.content)

        # Retrieve results
        entities = nlp.get_entities()
        categories = nlp.get_categories()
        metadata = nlp.get_metadata()
        nlp.calculate_avg()
        avg_score = nlp.get_avg_score()
        avg_magnitude = nlp.get_avg_magnitude()

        # nlp.check_clickbait(form.instance.title)

        # Create Category Models
        for category in categories.categories:
            Category.objects.create(
                article_id=article.pk,
                name=category.name,
                confidence=category.confidence,
            )

        # Create Entity Models
        for entity in entities.entities:
            e = Entity.objects.create(
                article_id=article.pk,
                name=entity.name,
                salience=round(entity.salience, 3),
                entity_type=enums.Entity.Type(entity.type).name,
            )

            if entity.metadata:
                if entity.metadata.get("wikipedia_url") and entity.metadata.get("mid"):
                    
                    # Knowledge base api call/handling
                    knowledge_results = requests.get("https://kgsearch.googleapis.com/v1/entities:search?ids=" + entity.metadata.get("mid") + "&key=AIzaSyBVWNLOTmBPy63hgF2ZgSLuOsFqFVRWSoQ&limit=1&indent=True")
                    json_results = knowledge_results.json().get('itemListElement')
                    results = json_results[0]['result']

                    # Get values from request
                    name = results.get('name')
                    desc = results.get('description')
                    image_details = results.get('image')
                    desc_details = results.get('detailedDescription')
                    url_details = results.get('url')

                    if (image_details):
                        image_content_url = image_details['contentUrl']
                        image_url = image_details['url']

                    # Get Detailed Description
                    if (desc_details):
                        article_body = desc_details['articleBody']
                        article_url = desc_details['url']

                    # Create Knowledge Model
                    Knowledge.objects.create(
                        entity_id=e.id,
                        name=name,
                        description=desc,
                        url=article_url,
                        article_body=article_body
                    )

                    MetaData.objects.create(
                        entity_id=e.id,
                        key=entity.metadata.get("wikipedia_url"),
                        value=entity.metadata.get("mid"),
                    )
                else:
                    MetaData.objects.create(entity_id=e.id, key="", value="")

        # Create Score Model
        Score.objects.create(
            article_id=article.pk, score=avg_score, magnitude=avg_magnitude
        )

        return super(ArticleCreate, self).form_valid(form)


class ArticleUpdate(UpdateView):
    model = Article
    fields = "__all__"


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy("article-list")


# =========================
# Authors
# =========================
class AuthorList(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author

    def get_object(self):
        obj = super().get_object()
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"


class AuthorUpdate(UpdateView):
    model = Author
    fields = "__all__"


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("author-list")


# =========================
# Publishers
# =========================
class PublisherArticleList(ListView):
    template_name = "app/articles_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
        return Article.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publisher"] = self.publisher
        return context


class PublisherDetailView(DetailView):
    model = Publisher


class PublisherList(ListView):
    model = Publisher
    context_object_name = "publisher_list"


class PublisherCreate(CreateView):
    model = Publisher
    fields = "__all__"


class PublisherUpdate(UpdateView):
    model = Publisher
    fields = "__all__"


class PublisherDelete(DeleteView):
    model = Publisher
    success_url = reverse_lazy("publisher-list")


# =========================
# Knowledge 
# =========================
class KnowledgeList(ListView):
    model = Knowledge


class KnowledgeDetailView(DetailView):
    model = Knowledge


# =========================
# Bookmarks
# =========================
class BookmarkListView(ListView):
    model = Bookmark

# =========================
# Utility 
# =========================
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):  
    user.profile.is_online = False
    user.profile.save()


def like(request):
    article_id = request.GET.get('article-id')
    operation = request.GET.get('operation')

    like, created = Like.objects.get_or_create(user=request.user, article_id=article_id)
    if operation == "like":
        like.is_liked = True
        like.save()
        data = {
            'Test': 'Like'
        }
    elif operation == "dislike":
        like.is_liked = False
        like.save()
        data = {
            'Test': 'Dislike'
        }

    return JsonResponse(data)


def favorite(request):
    article_id = request.GET.get('article-id')
    new_dislike, added = Favorite.objects.get_or_create(user=request.user, article_id=article_id)

    if added:
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def bookmark(request):
    article_id = request.GET.get('article-id')
    bookmark, bookmarked = Bookmark.objects.get_or_create(user=request.user, article_id=article_id)
    if not bookmark.is_bookmarked:
        bookmark.is_bookmarked = True
        bookmark.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)

def remove_bookmark(request):
    article_id = request.GET.get('article-id')
    bookmark = Bookmark.objects.get(user=request.user, article_id=article_id)
    print(bookmark.is_bookmarked)
    if bookmark.is_bookmarked:
        bookmark.is_bookmarked = False
        bookmark.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)

def add_rss_feed(request):
    rss_id = request.GET.get('rss-id')

    rss, added = RSS.objects.get_or_create(user=request.user, rss_id=rss_id)
    print(rss.feed_added)

    # Add feed if not added
    if not rss.feed_added:
        rss.feed_added = True
        rss.feed_removed = False
        rss.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def remove_rss_feed(request):
    rss_id = request.GET.get('rss-id')

    rss, removed = RSS.objects.get_or_create(user=request.user, rss_id=rss_id)

    # Remove feed if it has been added
    if not rss.feed_removed:
        rss.feed_added = False
        rss.feed_removed = True
        rss.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def get_popular_rss_articles(request):
    rss_id = request.GET.get('rss-id')
    rss_feed = RSSFeed.objects.get(pk=rss_id)

    if rss_feed:
        article_list = rss_feed.get_popular_article_list()
        article_data_list = []
        article_stats = {}
        for article in article_list:
            article_data = {
                'id': article.id,
                'rss_feed_id': article.rss_feed_id,
                'title': article.title,
                'publisher': article.publisher,
                'author': article.author,
                'content': article.content,
                'date': article.date
            }
            article_stats[article.id] = ('likes', article.get_likes(), 'comments', article.get_total_comments())
            article_data_list.append(article_data)
        data = {
            'Test': True,
            'article_list': article_data_list,
            'article_stats': article_stats,
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def get_latest_rss_articles(request):
    rss_id = request.GET.get('rss-id')
    rss_feed = RSSFeed.objects.get(pk=rss_id)

    if rss_feed:
        article_list = rss_feed.get_latest_article_list()
        article_data_list = []
        article_stats = {}
        for article in article_list:
            article_data = {
                'id': article.id,
                'rss_feed_id': article.rss_feed_id,
                'title': article.title,
                'publisher': article.publisher,
                'author': article.author,
                'content': article.content,
                'date': article.date
            }
            article_stats[article.id] = ('likes', article.get_likes(), 'comments', article.get_total_comments())
            article_data_list.append(article_data)
        data = {
            'Test': True,
            'article_list': article_data_list,
            'article_stats': article_stats,
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)

