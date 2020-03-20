import os
import requests
from django.utils import timezone
from django.urls import reverse_lazy
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
    RSSFeed,
    Like,
    Dislike,
    Favorite,
    Bookmark,
    RSS,
    SignUpForm
)

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/Users/spencerneveux/Desktop/FinalProject/theValidator/theValidator/app/api.json"


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
# Profile
# =========================
class ProfileUpdate(UpdateView):
    model = User
    fields = "__all__"
    success_url = reverse_lazy("article-list")
    template_name = "app/profile_form.html"


# =========================
# RSS Feeds
# =========================
class RSSList(ListView):
    model = RSSFeed

# =========================
# Articles
# =========================
class ArticleList(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article

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
    new_like, created = Like.objects.get_or_create(user=request.user, article_id=article_id)

    if created:
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def dislike(request):
    article_id = request.GET.get('article-id')
    new_dislike, created = Dislike.objects.get_or_create(user=request.user, article_id=article_id)

    if created:
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
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
    new_dislike, bookmarked = Bookmark.objects.get_or_create(user=request.user, article_id=article_id)

    if bookmarked:
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

def get_rss_articles(request):
    rss_id = request.GET.get('rss-id')
    rss_feed = RSSFeed.objects.get(pk=rss_id)

    if rss_feed:
        article_list = rss_feed.get_article_list().values()
        data = {
            'Test': True,
            'article_list': list(article_list)
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)