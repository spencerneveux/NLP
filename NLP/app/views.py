from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

from django.views.generic import ListView, DetailView

from .forms import ArticleForm
from .models import Author, Article, Publisher


# =========================
# Authors
# =========================
class AuthorList(ListView):
    model = Author


class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')


# =========================
# Articles
# =========================
class ArticleList(ListView):
    queryset = Article.objects.order_by("title")
    context_object_name = 'article_list'


class ArticleDetailView():
    model = Article

    def get_context_data(sefl, **kwargs):
        context = super().get_context_data(**kwargs)
        context['']


class ArticleView(FormView):
    template_name = 'app/article_form.html'
    form_class = ArticleForm
    success_url = '/article_list'

    def form_valid(self, form):
        return super().form_valid(form)


class ArticleCreate(CreateView):
    model = Article
    fields = '__all__'


class ArticleUpdate(UpdateView):
    model = Article
    fields = '__all__'


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article-list')


# =========================
# Publishers
# =========================
class PublisherArticleList(ListView):
    template_name = 'app/articles_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Article.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.publisher
        return context



