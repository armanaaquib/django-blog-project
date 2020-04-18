from django.test import TestCase
from django.urls import reverse
from accounts.models import UserProfile

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

    def test_user_created(self):
        form_data = {
            'username':'khan',
            'password':'jrk1',
            'confirm_password':'jrk1',
        }
        self.client.post(reverse('accounts:signUp'), data=form_data)

        self.assertTrue(UserProfile.objects.get(username='khan'))

    def test_view_success_url(self):
        form_data = {
            'username':'khan',
            'password':'jrk1',
            'confirm_password':'jrk1',
        }
        response = self.client.post(reverse('accounts:signUp'), data=form_data)
        
        self.assertRedirects(response, reverse('accounts:login'))

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

class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserProfile.objects.create_user(
            username='khan',
            password='jk-r',
        )
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        response = self.client.get(reverse('accounts:login'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:login'))

        self.assertTemplateUsed(response,'login.html')

    def test_is_authenticated(self):
        form_data = {
            'username':'khan',
            'password':'jk-r',
        }
        response = self.client.post(reverse('accounts:login'), data=form_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_is_not_authenticated(self):
        form_data = {
            'username':'khan',
            'password':'jk-s',
        }
        response = self.client.post(reverse('accounts:login'), data=form_data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_view_success_url(self):
        form_data = {
            'username':'khan',
            'password':'jk-r',
        }
        response = self.client.post(reverse('accounts:login'), data=form_data)
        
        self.assertRedirects(response, reverse('blog:post-list'))

class TestUserProfileDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserProfile.objects.create_user(
            first_name='John',
            last_name ='Ram',
            username='khan',
            password='jrk1',
            portfolio_site='https://www.google.com',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/accounts/profile/')
        
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get('/accounts/profile/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get(reverse('accounts:profile'))

        self.assertTemplateUsed(response,'userprofile_detail.html')

    def test_correct_context(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get(reverse('accounts:profile'), follow=True)

        self.assertEqual(response.context['user_profile'].full_name, 'John Ram')

class TestLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserProfile.objects.create_user(
            first_name='John',
            last_name ='Ram',
            username='khan',
            password='jrk1',
            portfolio_site='https://www.google.com',
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get('/accounts/logout/')
        
        self.assertRedirects(response, reverse('blog:post-list'))

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get(reverse('accounts:logout'))

        self.assertRedirects(response, reverse('blog:post-list'))

    def test_is_logout(self):
        self.client.login(username='khan', password='jrk1')
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('accounts:logout'))

        self.assertRedirects(response, '/accounts/login/?next=/accounts/logout/')
