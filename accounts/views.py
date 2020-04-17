from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
from .models import UserProfile
# Create your views here.

class SignUpView(FormView):
    template_name = 'signUp.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:signUp')

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
