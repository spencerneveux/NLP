import os
from django.utils import timezone
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.edit import (
    FormView,
    CreateView,
    DeleteView,
    UpdateView,
)

from django.views.generic import ListView, DetailView
from chartjs.views.lines import BaseLineChartView

from .forms import ArticleForm
from .models import Author, Article, Publisher, Score, Entity, Category
from .nlp import NLP

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/Users/spencerneveux/Desktop/FinalProject/NLP/NLP/app/api.json"


# =========================
# Articles
# =========================
class ArticleList(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["score_list"] = Score.objects.order_by("magnitude")
        context["entity_list"] = Entity.objects.order_by("name")
        context["category_list"] = Category.objects.order_by("name")
        return context


class ArticleView(FormView):
    template_name = "app/article_form.html"
    form_class = ArticleForm
    success_url = "/article_list"

    def form_valid(self, form):
        return super().form_valid(form)


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

        # Retrieve results
        entities = nlp.get_entities()
        categories = nlp.get_categories()

        # Create related DB models
        for category in categories.categories:
            Category.objects.create(
                article_id=article.pk,
                name=category.name,
                confidence=category.confidence,
            )

        for entity in entities.entities:
            Entity.objects.create(
                article_id=article.pk, name=entity.name, salience=entity.salience
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
# Misc
# =========================
class IndexView(ListView):
    template_name = "app/index.html"
    context_object_name = "article_list"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["score_list"] = Score.objects.order_by("magnitude")
        return context
