from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'username', 'password',
            'confirm_password', 'portfolio_site', 'profile_pic',
        )
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Passwords don't match"), code='pw not equal')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if authenticate(username=username, password=password) is None:
            raise forms.ValidationError(
                _('username or password is wrong'), 
                code='wrong login inputs'
            )
