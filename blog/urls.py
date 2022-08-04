from django.urls import re_path

from .views import (PostListView, PostDetailView,
                    PostCreateView, PostDraftListView,
                    UserPostListView, PostPublishView,
                    PostEditView, PostDeleteView)

app_name = 'blog'

urlpatterns = [
    re_path('^$', PostListView.as_view(), name='post-list'),
    re_path(r'^post/(?P<pk>\d+)', PostDetailView.as_view(), name='post-detail'),
    re_path(r'^new/', PostCreateView.as_view(), name='new'),
    re_path(r'^draft/', PostDraftListView.as_view(), name='draft'),
    re_path(r'^blogs/', UserPostListView.as_view(), name='user-posts'),
    re_path(r'^publish/(?P<pk>\d+)', PostPublishView.as_view(), name='publish'),
    re_path(r'^edit/(?P<pk>\d+)', PostEditView.as_view(), name='edit'),
    re_path(r'^delete/(?P<pk>\d+)', PostDeleteView.as_view(), name='delete'),
]
