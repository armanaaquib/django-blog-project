from django.test import TestCase
from accounts.models import UserProfile
# Create your tests here.

class TestUserProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_profile = UserProfile.objects.create_user(
            first_name='John',
            last_name ='Ram',
            username='khan',
            password='jrk1',
            portfolio_site='https://www.google.com',
        )
        user_profile.save()

    def test___str__(self):
        user_profile = UserProfile.objects.get(username='khan')
        
        self.assertEqual(user_profile.__str__(), '@khan')

    def test_full_name(self):
        user_profile = UserProfile.objects.get(username='khan')

        self.assertEqual(user_profile.full_name, 'John Ram')
