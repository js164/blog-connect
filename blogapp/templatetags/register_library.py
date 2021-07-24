from django import template
from blogapp.models import PostLike

register = template.Library()

@register.simple_tag
@register.filter(name='has_liked') 
def has_liked(user,post):
    try:
        like=PostLike.objects.get(post=post,like_by=user)
        return True
    except:
        return False

     