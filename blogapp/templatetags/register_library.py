from django import template
from blogapp.models import PostLike,Friends,Requestsend,UserProfile
from django.contrib.auth import get_user_model

User=get_user_model()

register = template.Library()

@register.simple_tag
@register.filter(name='has_liked') 
def has_liked(user,post):
    try:
        like=PostLike.objects.get(post=post,like_by=user)
        return True
    except:
        return False

@register.simple_tag
@register.filter(name='is_following') 
def is_following(user,pk):
    try:
        obj=Friends.objects.get(following=user,followers=User.objects.get(pk=pk))
        return True
    except:
        return False

@register.simple_tag
@register.filter(name='request_sended') 
def request_sended(user,pk):
    try:
        obj=Requestsend.objects.get(sendby=user,sendto=User.objects.get(pk=pk))
        return True
    except:
        return False

@register.simple_tag
@register.filter(name='can_view') 
def can_view(user,pk):
    if user.pk==pk:
        return True
    if 1==UserProfile.objects.filter(user=User.objects.get(pk=pk)).count():
        if UserProfile.objects.get(user=User.objects.get(pk=pk)).private_account:
            return False
        else:
            return True
    try:
        obj=Friends.objects.get(following=user,followers=User.objects.get(pk=pk))
        return True
    except:
        return False

@register.simple_tag
@register.filter(name='get_img') 
def get_img(user):
    try:
        obj=UserProfile.objects.get(user=user)
        return obj.photo
    except:
        return 'user.jpg'
        