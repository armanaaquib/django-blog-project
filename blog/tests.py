from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from unittest.mock import patch
import pytz
from .models import Post, Comment

test_datetime = timezone.datetime(2020, 4, 13, 7, 38, 20, 127325, tzinfo=pytz.UTC)
path_now = patch.object(timezone, 'now', return_value=test_datetime)
# Create your tests here.


class TestCommentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='john', password='jhn123')
        test_user.save()

        test_post = Post.objects.create(
            author=test_user,
            title='Test Post',
            text='This is a test post.',
            created_date=timezone.now()
        )
        test_post.save()

        test_comment = Comment.objects.create(
            post=test_post,
            author='Ram',
            text='test comment',
            created_date=timezone.now()
        )
        test_comment.save()

    def test_str(self):
        """
        test if __str__ returns text of the comment
        """
        comment = Comment.objects.get(author='Ram')
        self.assertEqual(comment.__str__(), 'test comment')

    def test_approve(self):
        """
        test if comment's approve_comment property become true
        """
        comment = Comment.objects.get(author='Ram')
        self.assertFalse(comment.approved_comment)
        comment.approve()
        self.assertTrue(comment.approved_comment)


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='john', password='jhn123')
        test_user.save()

        test_post = Post.objects.create(
            author=test_user,
            title='Test Post',
            text='This is a test post.',
            created_date=timezone.now()
        )
        test_post.save()

        test_comment = Comment.objects.create(
            post=test_post,
            author='Ram',
            text='test comment',
            created_date=timezone.now(),
            approved_comment=False
        )
        test_comment.save()

        test_comment = Comment.objects.create(
            post=test_post,
            author='Khan',
            text='test comment 2',
            created_date=timezone.now(),
            approved_comment=False
        )
        test_comment.save()

    def test_str(self):
        """
        test if __str__ returns title of the post
        """
        post = Post.objects.get(title='Test Post')
        self.assertEqual(post.__str__(), 'Test Post')

    def test_approved_comments(self):
        """
        test if returned approved comments
        """
        post = Post.objects.get(title='Test Post')

        comment = Comment.objects.get(author='Ram', post=post)
        comment.approve()

        approved_comments = Comment.objects.filter(post=post, approved_comment=True)
        self.assertSetEqual(post.approved_comments(), approved_comments)

    def test_publish(self):
        mock_now = path_now.start()
        post = Post.objects.get(title='Test Post')
        post.publish()
        self.assertEqual(post.published_date, timezone.datetime(2020, 4, 13, 7, 38, 20, 127325, tzinfo=pytz.UTC))
        mock_now.stop()
