from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'text')  
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDraftListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user, 
            published_date__isnull=False
        ).order_by('-published_date')

class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.publish()

        return redirect('blog:post-list')

class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'post_form.html'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:user-posts')
