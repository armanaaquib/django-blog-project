from django.urls import re_path,path
from .views import SignUpView, UserProfileDetailView, LoginView

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signUp/', SignUpView.as_view(), name='signUp'),
    re_path(r'^login/', LoginView.as_view(), name='login'),
    re_path(r'profile/', UserProfileDetailView.as_view(), name='profile'),
]
