from django.contrib import admin

# Register your models here.
from .models import Author, Publisher, Article, Score, Entity, Category, MetaData, Knowledge

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Score)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(MetaData)
admin.site.register(Knowledge)
