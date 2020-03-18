from django import template
from app.models import RSSFeed

register = template.Library()

@register.simple_tag
def get_rss_list(user):

    return user.get_rss_list()