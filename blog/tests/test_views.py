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
        response = self.client.post(reverse('blog:new'), data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Post.objects.last().title, 'Test Post')

    def test_redirects_to_desired_location(self):
        self.client.login(username='khan', password='jk-r')

        form_data = {
            'title': 'Test Post',
            'text': 'test text post'
        }
        response = self.client.post(reverse('blog:new'), data=form_data)

        self.assertRedirects(response, reverse('blog:draft'))

class TestPostDraftListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='khan',
            password='jk-r',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/draft/')
        
        self.assertRedirects(response, '/accounts/login/?next=/draft/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get('/draft/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:draft'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:draft'))

        self.assertTemplateUsed(response,'post_draft_list.html')

class TestUserPostListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='khan', password='jk-r')
        test_user2 = User.objects.create_user(username='ram', password='rs-l')

        test_post = Post.objects.create(
            author=test_user1,
            title='Test Post',
            text='This is a test post',
        )
        test_post.publish()
        test_post.save()

        test_post = Post.objects.create(
            author=test_user2,
            title='Test Post 2',
            text='This is a test post 2',
        )
        test_post.publish()
        test_post.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/blogs/')
        
        self.assertRedirects(response, '/accounts/login/?next=/blogs/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get('/blogs/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:user-posts'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:user-posts'))

        self.assertTemplateUsed(response,'post_list.html')

    def test_correct_context(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:user-posts'), follow=True)

        self.assertEqual(len(response.context['posts']), 1)

class TestPostPublishView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='khan', password='jk-r')

        test_post = Post.objects.create(
            author=test_user1,
            title='Test Post',
            text='This is a test post',
        )
        test_post.save()

        test_post = Post.objects.create(
            author=test_user1,
            title='Test Post 2',
            text='This is a test post 2',
        )
        test_post.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/publish/1')
        
        self.assertRedirects(response, '/accounts/login/?next=/publish/1')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get('/publish/1')
        
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:publish', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 302)

    def test_redirects_to_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:publish', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('blog:draft'))

class TestPostEditView(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='khan', password='jk-r')
        
        test_post = Post.objects.create(
            author=test_user1,
            title='Test Post',
            text='This is a test post',
        )
        test_post.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/edit/1')
        
        self.assertRedirects(response, '/accounts/login/?next=/edit/1')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get('/edit/1')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:edit', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:edit', kwargs={'pk': 1}))

        self.assertTemplateUsed(response,'post_form.html')

    def test_correct_context(self):
        self.client.login(username='khan', password='jk-r')

        response = self.client.get(reverse('blog:edit', kwargs={'pk': 1}), follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(list(response.context['form'].fields.keys()), ['title','text'])

    def test_post_edited(self):
        post = Post.objects.get(title='Test Post')

        self.client.login(username='khan', pasword='jk-r')

        form_data = {
            'title': 'Test Post edited',
            'text': 'This is a test post',
        }
        response = self.client.post(reverse('blog:edit', kwargs={'pk': 1}), data=form_data)
        self.assertEqual(response.status_code, 302)

        post.refresh_from_db()

        # self.assertEqual(post.title, 'Test Post edited')

class TestPostDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='khan', password='jk-r')

        test_post = Post.objects.create(
            author=test_user1,
            title='Test Post',
            text='This is a test post',
        )
        test_post.save()

        test_post = Post.objects.create(
            author=test_user1,
            title='Test Post 2',
            text='This is a test post 2',
        )
        test_post.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/delete/1')
        
        self.assertRedirects(response, '/accounts/login/?next=/delete/1')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get('/delete/1')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:delete', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.get(reverse('blog:delete', kwargs={'pk': 1}))

        self.assertTemplateUsed(response,'post_confirm_delete.html')

    def test_correct_context(self):
        self.client.login(username='khan', password='jk-r')

        response = self.client.get(reverse('blog:edit', kwargs={'pk': 1}), follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['post'].title, 'Test Post')

    def test_redirects_to_desired_location(self):
        self.client.login(username='khan', password='jk-r')
        response = self.client.post(reverse('blog:delete', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('blog:user-posts'))
