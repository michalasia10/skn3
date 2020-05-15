from django import template
register = template.Library()
from ..models import Post
from django.utils.safestring import mark_safe
import markdown
from ..views import post_search

@register.inclusion_tag('posts/latest.html')
def show_latest_post(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]

    return {'latest_posts':latest_posts}
@register.inclusion_tag('posts/newest.html')
def the_newest_post(count=1):
    newest = Post.published.order_by('-publish')[:count]
    return {'newest':newest}
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
