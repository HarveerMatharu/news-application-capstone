"""
Comprehensive unit tests for News Application API.

This module tests all API endpoints, permissions, authentication,
and business logic including signals for email and Twitter posting.
"""

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import Article, Newsletter, Publisher
from .tasks import send_article_notifications, post_to_twitter

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test User model and role assignment."""

    def setUp(self):
        """Create test users."""
        self.reader = User.objects.create_user(
            username='reader1',
            email='reader@test.com',
            password='testpass123',
            role='READER'
        )
        self.journalist = User.objects.create_user(
            username='journalist1',
            email='journalist@test.com',
            password='testpass123',
            role='JOURNALIST'
        )
        self.editor = User.objects.create_user(
            username='editor1',
            email='editor@test.com',
            password='testpass123',
            role='EDITOR'
        )

    def test_user_roles_created(self):
        """Test that users are created with correct roles."""
        self.assertEqual(self.reader.role, 'READER')
        self.assertEqual(self.journalist.role, 'JOURNALIST')
        self.assertEqual(self.editor.role, 'EDITOR')

    def test_user_group_assignment(self):
        """Test that users are automatically assigned to correct groups."""
        self.assertTrue(self.reader.groups.filter(name='Reader').exists())
        self.assertTrue(
            self.journalist.groups.filter(name='Journalist').exists()
        )
        self.assertTrue(self.editor.groups.filter(name='Editor').exists())


class ArticleAPITestCase(APITestCase):
    """Test Article API endpoints."""

    def setUp(self):
        """Create test data."""
        # Create users
        self.reader = User.objects.create_user(
            username='reader1',
            email='reader@test.com',
            password='testpass123',
            role='READER'
        )
        self.journalist = User.objects.create_user(
            username='journalist1',
            email='journalist@test.com',
            password='testpass123',
            role='JOURNALIST'
        )
        self.editor = User.objects.create_user(
            username='editor1',
            email='editor@test.com',
            password='testpass123',
            role='EDITOR'
        )

        # Create publisher
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='A test publisher'
        )

        # Create articles
        self.approved_article = Article.objects.create(
            title='Approved Article',
            content='This article is approved',
            author=self.journalist,
            approved=True,
            publisher=self.publisher
        )

        self.unapproved_article = Article.objects.create(
            title='Unapproved Article',
            content='This article is not approved',
            author=self.journalist,
            approved=False
        )

        # Setup API client
        self.client = APIClient()

    def test_reader_can_only_view_approved_articles(self):
        """Test that readers can only see approved articles."""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['title'],
            'Approved Article'
        )

    def test_journalist_can_see_all_articles(self):
        """Test that journalists can see all articles."""
        self.client.force_authenticate(user=self.journalist)
        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_editor_can_see_all_articles(self):
        """Test that editors can see all articles."""
        self.client.force_authenticate(user=self.editor)
        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_journalist_can_create_article(self):
        """Test that journalists can create articles."""
        self.client.force_authenticate(user=self.journalist)

        data = {
            'title': 'New Article',
            'content': 'This is a new article',
            'publisher_id': self.publisher.id
        }

        response = self.client.post('/api/articles/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Article')
        self.assertEqual(response.data['author']['username'], 'journalist1')

    def test_reader_cannot_create_article(self):
        """Test that readers cannot create articles."""
        self.client.force_authenticate(user=self.reader)

        data = {
            'title': 'New Article',
            'content': 'This is a new article'
        }

        response = self.client.post('/api/articles/', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_approve_article(self):
        """Test that editors can approve articles."""
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(
            f'/api/articles/{self.unapproved_article.id}/approve/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from database
        self.unapproved_article.refresh_from_db()
        self.assertTrue(self.unapproved_article.approved)

    def test_journalist_cannot_approve_article(self):
        """Test that journalists cannot approve articles."""
        self.client.force_authenticate(user=self.journalist)

        response = self.client.post(
            f'/api/articles/{self.unapproved_article.id}/approve/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_delete_article(self):
        """Test that editors can delete articles."""
        self.client.force_authenticate(user=self.editor)

        response = self.client.delete(
            f'/api/articles/{self.approved_article.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 1)

    def test_reader_cannot_delete_article(self):
        """Test that readers cannot delete articles."""
        self.client.force_authenticate(user=self.reader)

        response = self.client.delete(
            f'/api/articles/{self.approved_article.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_access_articles(self):
        """Test that unauthenticated users cannot access articles."""
        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):
    """Test subscription functionality."""

    def setUp(self):
        """Create test data."""
        # Create users
        self.reader = User.objects.create_user(
            username='reader1',
            email='reader@test.com',
            password='testpass123',
            role='READER'
        )
        self.journalist1 = User.objects.create_user(
            username='journalist1',
            email='journalist1@test.com',
            password='testpass123',
            role='JOURNALIST'
        )
        self.journalist2 = User.objects.create_user(
            username='journalist2',
            email='journalist2@test.com',
            password='testpass123',
            role='JOURNALIST'
        )

        # Create publishers
        self.publisher1 = Publisher.objects.create(
            name='Publisher 1',
            description='First publisher'
        )
        self.publisher2 = Publisher.objects.create(
            name='Publisher 2',
            description='Second publisher'
        )

        # Create articles
        self.article1 = Article.objects.create(
            title='Article from Publisher 1',
            content='Content',
            author=self.journalist1,
            approved=True,
            publisher=self.publisher1
        )
        self.article2 = Article.objects.create(
            title='Article from Journalist 2',
            content='Content',
            author=self.journalist2,
            approved=True
        )
        self.article3 = Article.objects.create(
            title='Article from Publisher 2',
            content='Content',
            author=self.journalist1,
            approved=True,
            publisher=self.publisher2
        )

        # Subscribe reader to publisher1 and journalist2
        self.reader.subscribed_publishers.add(self.publisher1)
        self.reader.subscribed_journalists.add(self.journalist2)

        self.client = APIClient()

    def test_reader_can_retrieve_subscribed_content(self):
        """Test that readers only see articles from their subscriptions."""
        self.client.force_authenticate(user=self.reader)

        response = self.client.get('/api/articles/subscribed/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check that correct articles are returned
        titles = [article['title'] for article in response.data]
        self.assertIn('Article from Publisher 1', titles)
        self.assertIn('Article from Journalist 2', titles)
        self.assertNotIn('Article from Publisher 2', titles)

    def test_non_reader_cannot_access_subscribed_endpoint(self):
        """Test that non-readers cannot access subscribed endpoint."""
        self.client.force_authenticate(user=self.journalist1)

        response = self.client.get('/api/articles/subscribed/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NewsletterAPITestCase(APITestCase):
    """Test Newsletter API endpoints."""

    def setUp(self):
        """Create test data."""
        self.reader = User.objects.create_user(
            username='reader1',
            password='testpass123',
            role='READER'
        )
        self.journalist = User.objects.create_user(
            username='journalist1',
            password='testpass123',
            role='JOURNALIST'
        )
        self.editor = User.objects.create_user(
            username='editor1',
            password='testpass123',
            role='EDITOR'
        )

        # Create article
        self.article = Article.objects.create(
            title='Test Article',
            content='Content',
            author=self.journalist,
            approved=True
        )

        self.client = APIClient()

    def test_journalist_can_create_newsletter(self):
        """Test that journalists can create newsletters."""
        self.client.force_authenticate(user=self.journalist)

        data = {
            'title': 'Weekly Newsletter',
            'description': 'This week\'s top stories',
            'article_ids': [self.article.id]
        }

        response = self.client.post(
            '/api/newsletters/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Newsletter.objects.count(), 1)

    def test_reader_cannot_create_newsletter(self):
        """Test that readers cannot create newsletters."""
        self.client.force_authenticate(user=self.reader)

        data = {
            'title': 'Weekly Newsletter',
            'description': 'This week\'s top stories'
        }

        response = self.client.post('/api/newsletters/', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_update_newsletter(self):
        """Test that editors can update newsletters."""
        newsletter = Newsletter.objects.create(
            title='Original Title',
            description='Original Description',
            author=self.journalist
        )

        self.client.force_authenticate(user=self.editor)

        data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }

        response = self.client.patch(
            f'/api/newsletters/{newsletter.id}/',
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newsletter.refresh_from_db()
        self.assertEqual(newsletter.title, 'Updated Title')


class SignalTestCase(TestCase):
    """Test signal functionality for email and Twitter posting."""

    def setUp(self):
        """Create test data."""
        self.journalist = User.objects.create_user(
            username='journalist1',
            email='journalist@test.com',
            password='testpass123',
            role='JOURNALIST'
        )
        self.reader = User.objects.create_user(
            username='reader1',
            email='reader@test.com',
            password='testpass123',
            role='READER'
        )

        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='Description'
        )

        # Subscribe reader to journalist
        self.reader.subscribed_journalists.add(self.journalist)

    @patch('news.tasks.send_mass_mail')
    def test_email_sent_on_article_approval(self, mock_send_mail):
        """Test that email is sent when article is approved."""
        article = Article.objects.create(
            title='Test Article',
            content='Test content',
            author=self.journalist,
            approved=False
        )

        # Approve the article (should trigger signal)
        article.approved = True
        article.save()

        # Check that send_mass_mail was called
        mock_send_mail.assert_called_once()

    @override_settings(TWITTER_BEARER_TOKEN='test_token_12345')
    @patch('news.tasks.requests.post')
    def test_twitter_post_on_article_approval(self, mock_post):
        """Test that tweet is posted when article is approved."""
        # Mock successful Twitter response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'data': {'id': '123456'}}
        mock_post.return_value = mock_response

        article = Article.objects.create(
            title='Test Article',
            content='Test content',
            author=self.journalist,
            approved=False
        )

        # Approve the article (should trigger signal)
        article.approved = True
        article.save()

        # Check that requests.post was called
        self.assertTrue(mock_post.called)

        # Verify it was called with the Twitter API endpoint
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], 'https://api.twitter.com/2/tweets')


class JWTAuthenticationTestCase(APITestCase):
    """Test JWT authentication."""

    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='READER'
        )

    def test_obtain_jwt_token(self):
        """Test obtaining JWT token."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        response = self.client.post('/api/token/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_api_with_token(self):
        """Test accessing API with JWT token."""
        # Obtain token
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        token_response = self.client.post('/api/token/', data)
        access_token = token_response.data['access']

        # Use token to access API
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self):
        """Test that invalid credentials are rejected."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = self.client.post('/api/token/', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
