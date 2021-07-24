from django.conf.urls import url
from blogapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url(r'^$',views.PostListView.as_view(),name='post_list'),
    url(r'^myposts/$',views.MyPost.as_view(),name='mypost'),
    url(r'^about/$',views.AboutView.as_view(),name='about'),
    url(r'^signup/$',views.UserSignUp.as_view(),name='signup'),
    url('post/(?P<pk>\d+)$',views.PostDetailView.as_view(),name='post_detail'),
    url(r'^post/create/$',views.CreatePostView.as_view(),name='post_create'),
    url(r'^post/(?P<pk>\d+)/update$',views.PostUpdateView.as_view(),name='post_update'),
    url(r'^post/(?P<pk>\d+)/delete$',views.PostDeleteView.as_view(),name='post_delete'),
    url(r'^post/draft/$',views.PostDraftView.as_view(),name='post_draft_list'),
    url('post/(?P<pk>\d+)/publish$',views.post_publish,name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/add$',views.comment_create,name='comment_create'),
    url(r'^like$',views.like_post,name='like_post'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)