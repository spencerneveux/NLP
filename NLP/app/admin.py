from django.contrib import admin

# Register your models here.
from .models import Author, Publisher, Article

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Article)