from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from .models import Post

# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'

    def get_queryset(self):
        published_posts = Post.objects.filter(published_date__lte=timezone.now())
        return published_posts.order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
