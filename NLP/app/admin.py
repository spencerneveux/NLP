from django.contrib import admin

# Register your models here.
from .models import Author, Publication, Article

admin.site.register(Author)
admin.site.register(Publication)
admin.site.register(Article)