from django.test import TestCase
from blog.forms import PostForm, CommentForm


class TestPostForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        data = {'title': 'Test Post', 'text': 'This is a test post.'}
        cls.post_form = PostForm(data=data)

    def setUp(self):
        self.assertTrue(self.post_form.is_valid())

    def test_title(self):
        self.assertEqual(self.post_form.cleaned_data['title'], 'Test Post')

    def test_text(self):
        text = 'This is a test post.'
        self.assertEqual(self.post_form.cleaned_data['text'], text)


class TestCommentForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        data = {'author': 'Ram', 'text': 'This is a test comment.'}
        cls.comment_form = CommentForm(data=data)

    def setUp(self):
        self.assertTrue(self.comment_form.is_valid())

    def test_author(self):
        self.assertEqual(self.comment_form.cleaned_data['author'], 'Ram')
        pass

    def test_text(self):
        text = 'This is a test comment.'
        self.assertEqual(self.comment_form.cleaned_data['text'], text)

