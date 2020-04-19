from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from blog.models import Post, Comment

class TestPostListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='john', password='j-kl')
        test_user.save()
        test_user2 = User.objects.create_user(username='khan', password='k-ml')
        test_user2.save()

        test_post = Post.objects.create(
            author=test_user,
            title="Test Post", 
            text="this is a test post",
            created_date=timezone.now(),
            published_date=timezone.now(),
        )
        test_post.save()

        test_post = Post.objects.create(
            author=test_user2,
            title="Test Post2", 
            text="this is a test post 2",
            created_date=timezone.now(),
            published_date=timezone.now(),
        )
        test_post.save()

        test_post = Post.objects.create(
            author=test_user2,
            title="Test Post2", 
            text="this is a test post 2",
            created_date=timezone.now(),
        )
        test_post.save()

    def test_correct_context(self):
        response = self.client.get(reverse('blog:post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 2)

    def test_correct_template(self):
        response = self.client.get(reverse('blog:post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_list.html')


class TestPostDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='john', password='j-kl')
        test_user.save()

        test_post = Post.objects.create(
            author=test_user,
            title="Test Post", 
            text="this is a test post",
        )
        test_post.save()

        test_comment = Comment.objects.create(
            post=test_post,
            author="Test Comment",
            text="This is a test comment."
        )
        test_comment.save()

    def test_correct_context(self):
        response = self.client.get(reverse('blog:post-detail', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'].title, 'Test Post')
        self.assertEqual(len(response.context['post'].comments.all()), 1)

    def test_correct_template(self):
        response = self.client.get(reverse('blog:post-detail', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')

class PostCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='khan',
            password='jk-r',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/new/')
        
        self.assertRedirects(response, '/accounts/login/?next=/new/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get('/new/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:new'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:new'))

        self.assertTemplateUsed(response,'post_form.html')

    def test_post_created(self):
        self.client.login(username='khan', password='jk-r')

        form_data = {
            'title': 'Test Post',
            'text': 'test text post'
        }
        self.client.post(reverse('blog:new'), data=form_data)

        self.assertTrue(Post.objects.get(title='Test Post'))
