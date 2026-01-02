"""
API views for the news application.

This module contains all ViewSets for the REST API endpoints including
Article, Newsletter, Publisher, and User management.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article, Newsletter, Publisher, User
from .serializers import (
    ArticleSerializer,
    NewsletterSerializer,
    PublisherSerializer,
    UserSerializer
)
from .permissions import (
    IsJournalist,
    IsEditor,
    IsEditorOrJournalist,
    IsOwnerOrReadOnly
)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Article model with role-based access control.

    Endpoints:
    - GET /api/articles/ - List all approved articles
    - GET /api/articles/subscribed/ - User's subscribed content
    - GET /api/articles/<id>/ - Single article detail
    - POST /api/articles/ - Create article (journalists only)
    - PUT /api/articles/<id>/ - Update article (editors/journalists)
    - DELETE /api/articles/<id>/ - Delete article (editors/journalists)
    """

    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return articles based on user role.

        Readers see only approved articles.
        Editors and Journalists see all articles.

        Returns:
            QuerySet: Filtered article queryset based on user role
        """
        user = self.request.user

        if user.role == 'READER':
            return Article.objects.filter(approved=True)
        else:
            return Article.objects.all()

    def get_permissions(self):
        """
        Assign permissions based on action.

        Returns:
            list: List of permission instances for the current action
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsJournalist]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsEditorOrJournalist]
        elif self.action == 'approve':
            permission_classes = [IsAuthenticated, IsEditor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def subscribed(self, request):
        """
        Return articles from user's subscribed publishers and journalists.

        Only available to readers.

        Args:
            request: The HTTP request object

        Returns:
            Response: Serialized list of subscribed articles
        """
        user = request.user

        if user.role != 'READER':
            return Response(
                {"detail": "Only readers can access subscribed content."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get articles from subscribed publishers
        publisher_articles = Article.objects.filter(
            publisher__in=user.subscribed_publishers.all(),
            approved=True
        )

        # Get articles from subscribed journalists
        journalist_articles = Article.objects.filter(
            author__in=user.subscribed_journalists.all(),
            approved=True
        )

        # Combine and remove duplicates
        articles = (publisher_articles | journalist_articles).distinct()

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve an article. Only editors can approve.

        This triggers email notifications and X posting via signals.

        Args:
            request: The HTTP request object
            pk: Primary key of the article to approve

        Returns:
            Response: Serialized approved article or error message
        """
        article = self.get_object()

        if article.approved:
            return Response(
                {"detail": "Article is already approved."},
                status=status.HTTP_400_BAD_REQUEST
            )

        article.approved = True
        article.save()  # This triggers the post_save signal

        serializer = self.get_serializer(article)
        return Response(serializer.data)


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Newsletter model.

    Journalists and Editors can create/edit.
    Readers can only view.
    """

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Assign permissions based on action.

        Returns:
            list: List of permission instances for the current action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsEditorOrJournalist]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Publisher model.

    Read-only for all authenticated users.
    """

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User model.

    Read-only for all authenticated users with subscription management.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Return current user details.

        Args:
            request: The HTTP request object

        Returns:
            Response: Serialized current user data
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def subscribe_publisher(self, request, pk=None):
        """
        Subscribe to a publisher (readers only).

        Args:
            request: The HTTP request object
            pk: Primary key of the publisher to subscribe to

        Returns:
            Response: Success message or error
        """
        user = request.user

        if user.role != 'READER':
            return Response(
                {"detail": "Only readers can subscribe."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            publisher = Publisher.objects.get(pk=pk)
            user.subscribed_publishers.add(publisher)
            return Response(
                {"detail": f"Subscribed to {publisher.name}"}
            )
        except Publisher.DoesNotExist:
            return Response(
                {"detail": "Publisher not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def subscribe_journalist(self, request, pk=None):
        """
        Subscribe to a journalist (readers only).

        Args:
            request: The HTTP request object
            pk: Primary key of the journalist to subscribe to

        Returns:
            Response: Success message or error
        """
        user = request.user

        if user.role != 'READER':
            return Response(
                {"detail": "Only readers can subscribe."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            journalist = User.objects.get(pk=pk, role='JOURNALIST')
            user.subscribed_journalists.add(journalist)
            return Response(
                {"detail": f"Subscribed to {journalist.username}"}
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Journalist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
