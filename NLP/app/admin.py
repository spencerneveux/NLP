from django.contrib import admin

# Register your models here.
from .models import Author, Publisher, Article, Score, Entity, Category

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Score)
admin.site.register(Entity)
admin.site.register(Category)
