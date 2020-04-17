from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import UserProfile
from accounts.forms import SignUpForm, LoginForm

class TestSignUpForm(TestCase):
    def test_form_valid_for_minimum_inputs(self):
        form_data = {
            'username':'khan',
            'password':'jrk1',
            'confirm_password':'jrk1',
        }
        signUp_form = SignUpForm(data=form_data)

        self.assertTrue(signUp_form.is_valid())

    def test_if_passwords_do_not_match(self):
        form_data = {
            'username':'khan',
            'password':'jrk1',
            'confirm_password':'jrk2',
        }
        signUp_form = SignUpForm(data=form_data)

        self.assertFalse(signUp_form.is_valid())

        try:
            signUp_form.clean()
        except ValidationError as e:
            self.assertEqual(e.code, 'pw not equal')

class TestLoginForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserProfile.objects.create_user(
            username='khan',
            password='jk-r',
        )

    def test_for_valid_user(self):
        form_data = {
            'username':'khan',
            'password':'jk-r',
        }
        login_form = LoginForm(data=form_data)

        self.assertTrue(login_form.is_valid())

    def test_for_invalid_username(self):
        form_data = {
            'username':'khans',
            'password':'jk-r',
        }
        login_form = LoginForm(data=form_data)

        self.assertFalse(login_form.is_valid())

        try:
            login_form.clean()
        except ValidationError as e:
            self.assertEqual(e.code, 'wrong login inputs')

    def test_for_invalid_password(self):
        form_data = {
            'username':'khan',
            'password':'jk-s',
        }
        login_form = LoginForm(data=form_data)

        self.assertFalse(login_form.is_valid())

        try:
            login_form.clean()
        except ValidationError as e:
            self.assertEqual(e.code, 'wrong login inputs')
