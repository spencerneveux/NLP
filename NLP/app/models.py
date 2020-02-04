from django.db import models
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class Author(models.Model):
    number_articles = models.IntegerField(default=0)
    articles = models.CharField(max_length=200, default="default")
    author_name = models.CharField(max_length=200, default="default")
    work_history = models.CharField(max_length=200, default="default")
    social_media = models.CharField(max_length=200, default="default")
    nationality = models.CharField(max_length=200, default="default")


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class Publication(models.Model):
    publisher_name = models.CharField(max_length=200, default="default")
    rss_feed = models.CharField(max_length=200, default="default")
    picture = models.CharField(max_length=200, default="default")
    abbreviation = models.CharField(max_length=200, default="default")
    website = models.CharField(max_length=200, default="default")
    funding = models.CharField(max_length=200, default="default")
    number_authors = models.IntegerField(default=0)


class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = '__all__'


class Article(models.Model):
    title = models.CharField(max_length=200, default="default")
    content = models.TextField()
    author = models.CharField(max_length=200, default="default")
    publisher = models.CharField(max_length=200, default="default")


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
