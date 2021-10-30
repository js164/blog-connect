from django.contrib import admin
from .models import Post,Comment,PostLike,Requestsend,Friends,UserProfile
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(Requestsend)
admin.site.register(Friends)
admin.site.register(UserProfile)
