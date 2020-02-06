from django.utils.timezone import now
from django.db import models
from django.forms import ModelForm
from django.urls import reverse


# =========================
# Authors
# =========================
class Author(models.Model):
    name = models.CharField(max_length=200, default="")
    number_articles = models.IntegerField(default=0)
    articles = models.CharField(max_length=200, default="")
    work_history = models.CharField(max_length=200, default="")
    social_media = models.CharField(max_length=200, default="")
    nationality = models.CharField(max_length=200, default="")
    last_accessed = models.DateTimeField(default=now)

    class Meta:
        ordering = ["-name"]

    # Used by generic view to redirect
    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


# =========================
# Publisher
# =========================
class Publisher(models.Model):
    name = models.CharField(max_length=200, default="")
    rss_feed = models.CharField(max_length=200, default="")
    picture = models.CharField(max_length=200, default="")
    abbreviation = models.CharField(max_length=200, default="")
    website = models.CharField(max_length=200, default="")
    funding = models.CharField(max_length=200, default="")
    number_authors = models.IntegerField(default=0)

    class Meta:
        ordering = ["-name"]

    # Used by generic view to redirect
    def get_absolute_url(self):
        return reverse("publisher-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


# =========================
# Articles
# =========================
class Article(models.Model):
    author = models.CharField(max_length=200, default="")
    publisher = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200, default="")
    content = models.TextField()

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = "__all__"


# =========================
# Score
# =========================
class Score(models.Model):
    article = models.OneToOneField(
        Article, on_delete=models.CASCADE, primary_key=True
    )
    magnitude = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
