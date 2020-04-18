from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import SignUpForm, LoginForm
from .models import UserProfile
# Create your views here.

class SignUpView(FormView):
    template_name = 'signUp.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        userProfile = form.save()
        userProfile.set_password(userProfile.password)
        userProfile.save()
        return super().form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']

        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super().form_valid(form)

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'userprofile_detail.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return get_object_or_404(UserProfile, username=self.request.user.username)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('blog:post-list'))
