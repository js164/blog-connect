from django.conf.urls import url
from blogapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url(r'^$',views.PostListView.as_view(),name='post_list'),
    url(r'^myposts/$',views.MyPost.as_view(),name='mypost'),
    url(r'^signup/$',views.UserSignUp.as_view(),name='signup'),
    url('post/(?P<pk>\d+)$',views.PostDetailView.as_view(),name='post_detail'),
    url(r'^post/create/$',views.CreatePostView.as_view(),name='post_create'),
    url(r'^post/(?P<pk>\d+)/update$',views.PostUpdateView.as_view(),name='post_update'),
    url(r'^post/(?P<pk>\d+)/delete$',views.PostDeleteView.as_view(),name='post_delete'),
    url(r'^post/draft/$',views.PostDraftView.as_view(),name='post_draft_list'),
    url('post/(?P<pk>\d+)/publish$',views.post_publish,name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/add$',views.comment_create.as_view(),name='comment_create'),
    url(r'^like$',views.like_post,name='like_post'),
    url(r'userprofile/(?P<pk>\d+)$',views.UserProfileView.as_view(),name='userprofile'),
    url(r'updateprofile/(?P<pk>\d+)$',views.UpdateProfile.as_view(),name='updateprofile'),
    url(r'editprofile/',views.EditProfile.as_view(),name='editprofile'),
    url(r'profile/(?P<pk>\d+)$',views.Profile.as_view(),name='profile'),
    url(r'requestsend/(?P<pk>\d+)$',views.SendRequest.as_view(),name='requestsend'),
    url(r'requestconfirem/(?P<pk>\d+)$',views.ConfirmRequest.as_view(),name='requestconfirem'),
    url(r'unfollow/(?P<pk>\d+)$',views.Unfollow.as_view(),name='unfollow'),
    url(r'requestdeletebysender/(?P<pk>\d+)$',views.DeleteRequestBySender.as_view(),name='requestdeletebysender'),
    url(r'requestdeletebyreciver/(?P<pk>\d+)$',views.DeleteRequestByReciver.as_view(),name='requestdeletebyreciver'),
    url(r'requests/',views.AllRequests.as_view(),name='requests'),
    url(r'followers/',views.Showfollowers.as_view(),name='followers'),
    url(r'following/',views.Showfollowing.as_view(),name='following'),
    url(r'finduser/',views.FindUser.as_view(),name='finduser'),
    url(r'explore/',views.Explore.as_view(),name='explore'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)