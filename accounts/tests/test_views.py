from django.test import TestCase
from django.urls import reverse
from accounts.views import SignUpView

class TestSignUpView(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signUp/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        response = self.client.get(reverse('accounts:signUp'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:signUp'))

        self.assertTemplateUsed(response,'signUp.html')

    def test_view_success_url(self):
        form_data = {
            'username':'khan',
            'password':'jrk1',
            'confirm_password':'jrk1',
        }
        response = self.client.post(reverse('accounts:signUp'), data=form_data)
        
        self.assertRedirects(response, reverse('accounts:signUp'))

    def test_form_if_password_is_less_than_4(self):
        form_data = {
            'username':'khan',
            'password':'jrk',
            'confirm_password':'jrk',
        }
        response = self.client.post(reverse('accounts:signUp'), data=form_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response=response, 
            form='form', 
            field='password', 
            errors=['This password is too short. It must contain at least 4 characters.',]
        )