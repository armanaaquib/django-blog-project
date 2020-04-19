from django.urls import re_path, path
from .views import PostListView, PostDetailView, PostCreateView

app_name = 'blog'

urlpatterns = [
    re_path('^$', PostListView.as_view(), name='post-list'),
    re_path(r'^post/(?P<pk>\d+)', PostDetailView.as_view(), name='post-detail'),
    re_path(r'^new/', PostCreateView.as_view(), name='new'),
]
