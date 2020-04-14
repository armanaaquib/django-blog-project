from django.urls import re_path, path
from . import views

app_name = 'blog'

urlpatterns = [
    re_path('^$', views.PostListView.as_view(), name='post-list'),
    re_path(r'^post/(?P<pk>\d+)', views.PostDetailView.as_view(), name='post-detail'),
]
