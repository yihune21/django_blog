from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Category, Comment

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            body='This is a test post body',
            excerpt='Test excerpt',
            published=True
        )
        self.post.categories.add(self.category)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.published)

    def test_post_slug_generation(self):
        self.assertEqual(self.post.slug, 'test-post')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            body='Test body',
            published=True
        )
        self.comment = Comment.objects.create(
            author='Test Author',
            body='Test comment',
            post=self.post
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.author, 'Test Author')
        self.assertEqual(self.comment.post, self.post)

    def test_comment_str(self):
        expected = f" Test Author on {self.post} "
        self.assertEqual(str(self.comment), expected)

class BlogViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            body='Test body content',
            published=True
        )
        self.post.categories.add(self.category)

    def test_blog_index_view(self):
        response = self.client.get(reverse('blog_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test body content')

    def test_blog_category_view(self):
        response = self.client.get(reverse('blog_category', args=['Test Category']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_blog_search_view(self):
        response = self.client.get(reverse('blog_search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_comment_submission(self):
        response = self.client.post(
            reverse('blog_detail', args=[self.post.pk]),
            {
                'author': 'Test Commenter',
                'body': 'This is a test comment'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                author='Test Commenter',
                body='This is a test comment'
            ).exists()
        )

    def test_pagination(self):
        for i in range(10):
            Post.objects.create(
                title=f'Post {i}',
                author=self.user,
                body=f'Body {i}',
                published=True
            )
        response = self.client.get(reverse('blog_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 5)