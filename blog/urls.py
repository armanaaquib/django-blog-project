from django.urls import re_path
from . import views

app_name = 'blog'

urlpatterns = [
    re_path('^$', views.PostListView.as_view(), name="post-list"),
]
