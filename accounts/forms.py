from django import forms
from django.contrib.auth.password_validation import validate_password
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
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match", code='pw not equal')
