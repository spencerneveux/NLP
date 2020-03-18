from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import (
	Author, 
	Publisher, 
	Article, 
	Score, 
	Entity, 
	Category, 
	MetaData, 
	Knowledge,
	Profile,
	RSSFeed,
	Status
	)


class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Score)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(MetaData)
admin.site.register(Knowledge)
admin.site.register(RSSFeed)
