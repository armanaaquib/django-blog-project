from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import SignUpForm
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
