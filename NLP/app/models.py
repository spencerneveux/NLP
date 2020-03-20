from django.utils.timezone import now
from django import forms
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver


# =========================
# Profile
# =========================
class ProfileManager(models.Manager):
    def create_profile(self, upload, description):
        profile = self.create(
            upload=upload, description=description
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to="app/static/images", default="static/images/default.png")
    description = models.CharField(max_length=200, default="", null=True)
    is_online = models.BooleanField(default=False)
    signup_confirmation = models.BooleanField(default=False)

    def get_rss_list(self):
        return self.user.rss_set.all()

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, help_text='First Name')
    last_name = forms.CharField(max_length=200, help_text='Last Name')
    email = forms.EmailField(max_length=200, help_text='Email')

    class Meta: 
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


# =========================
# RSS Feed
# =========================
class RSSFeed(models.Model):
    name = models.CharField(max_length=200, default="")
    link = models.URLField(max_length=200, default="")

    def get_article_list(self):
        return self.article_set.all()

    def __str__(self):
        return self.name


# =========================
# Articles
# =========================
class ArticleManager(models.Manager):
    def create_article(self, author, publisher, title, content):
        article = self.create(
            author=author, publisher=publisher, title=title, content=content
        )
        return article


class Article(models.Model):
    objects = ArticleManager()
    rss_feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=200, default="")
    publisher = models.CharField(max_length=200, default="")
    author = models.CharField(max_length=200, default="")
    content = models.TextField()

    def get_entities(self):
        return self.entity_set.all()

    def get_categories(self):
        return self.category_set.all()

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})

    def test_method(self):
        return "Test"

    def __str__(self):
        return f'Title: {self.title}'


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = "__all__"


# =========================
# Authors
# =========================
class AuthorManager(models.Manager):
    def create_author(self, author):
        a = self.create(
            name=author.name,
            number_articles=author.number_articles,
            social_media=author.social_media,
            last_accessed=author.last_accessed,
        )
        return a


class Author(models.Model):
    name = models.CharField(max_length=200, default="")
    number_articles = models.IntegerField(default=0)
    social_media = models.CharField(max_length=200, default="")
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
class PublisherManager(models.Manager):
    def create_publisher(self, publisher):
        p = self.create(
            name=publisher.name,
            rss_feed=publisher.rss_feed,
            picture=publisher.picture,
            abbreviation=publisher.abbreviation,
            website=publisher.website,
        )
        return p


class Publisher(models.Model):
    name = models.CharField(max_length=200, default="")
    rss_feed = models.CharField(max_length=200, default="")
    picture = models.CharField(max_length=200, default="")
    abbreviation = models.CharField(max_length=200, default="")
    website = models.CharField(max_length=200, default="")

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
# Score
# =========================
class ScoreManager(models.Model):
    def create_score(self, magnitude, score):
        score = self.create(magnitude=magnitude, score=score)
        return score


class Score(models.Model):
    objects = ScoreManager()
    article = models.OneToOneField(Article, on_delete=models.CASCADE, primary_key=True)
    magnitude = models.FloatField(default=0)
    score = models.FloatField(default=0)

    def __str__(self):
        return "Score to string"


# =========================
# Entity
# =========================
class EntityManager(models.Manager):
    def create_entity(self, name):
        e = self.create(name=name)
        return e

    def get_metadata(self):
        return self.metadata_set.all()


class Entity(models.Model):
    objects = EntityManager()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, default="")
    entity_type = models.CharField(max_length=200, default="")
    salience = models.FloatField(default=0, null=True)
    wiki = models.URLField(max_length=200, default="", null=True)
    mid = models.CharField(max_length=200, default="", null=True)

    def __str__(self):
        return self.name


# =========================
# Knowledge 
# =========================
class KnowledgeManager(models.Manager):
    def create_knowledge(self, name, description, url, article_body):
        knowledge = self.create(name=name, description=description, url=url, article_body=article_body)
        return knowledge


class Knowledge(models.Model):
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="", null=True)
    url = models.URLField(max_length=200, default="")
    article_body = models.TextField()

    def __str__(self):
        return self.name


# =========================
# Categories
# =========================
class CategoryManager(models.Manager):
    def create_category(self, name, confidence):
        category = self.create(name=name, confidence=confidence)
        return category


class Category(models.Model):
    objects = CategoryManager()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="")
    confidence = models.FloatField(default=0)

    def __str__(self):
        return self.name


# =========================
# Interactions
# =========================
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=200, default="")


class RSS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rss = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    feed_added = models.BooleanField(default=False)
    feed_removed = models.BooleanField(default=True)

    def get_rss_status(self):
        if self.feed_added == True:
            return True
        else:
            return False

    def get_article_list(self):
        return self.rss.get_article_list()

    def __str__(self):
        return self.rss.name

# =========================
# Status
# =========================
class Status(models.Manager):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, primary_key=True)
    read = models.BooleanField(default=False)
    bookmark = models.BooleanField(default=False)

    def __str__(self):
        return self.read


# =========================
# Meta Data
# =========================
class MetaDataManager(models.Manager):
    def create_metadata(self, key, value):
        meta_data = self.create(key=key, value=value)
        return meta_data


class MetaData(models.Model):
    objects = MetaDataManager()
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True)
    key = models.CharField(max_length=200, default="")
    value = models.CharField(max_length=200, default="")

    def __str__(self):
        return f"Key: {self.key} Value: {self.value}"
