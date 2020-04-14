from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Post

# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
