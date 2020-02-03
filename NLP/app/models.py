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
        fields = ['number_articles', 'author_name']

    # def __init__(self, *args, **kwargs):
    #     super.__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Search Author'))


class Publication(models.Model):
    number_articles = models.IntegerField(default=0)
    rss_feed = models.CharField(max_length=200, default="default")
    picture = models.CharField(max_length=200, default="default")
    abbreviation = models.CharField(max_length=200, default="default")
    website = models.CharField(max_length=200, default="default")
    funding = models.CharField(max_length=200, default="default")
    sponsor = models.CharField(max_length=200, default="default")
    number_authors = models.IntegerField(default=0)


