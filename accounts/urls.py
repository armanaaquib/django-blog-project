from django.urls import re_path
from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signUp/', SignUpView.as_view(), name='signUp'),
]