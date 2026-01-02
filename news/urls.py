"""
URL configuration for the news application.

This module defines both API endpoints and web interface routes.
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from . import views
from . import web_views


# Create router for API endpoints
router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')
router.register(r'newsletters', views.NewsletterViewSet, basename='newsletter')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'users', views.UserViewSet, basename='user')

app_name = 'news'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='news/login.html'), name='login'),
    path('logout/', web_views.logout_view, name='logout'),

    # Web interface routes - Articles
    path('', web_views.article_list, name='article_list'),
    path('articles/', web_views.article_list, name='article_list'),
    path('articles/pending/', web_views.pending_articles, name='pending_articles'),
    path('articles/subscribed/', web_views.subscribed_articles, name='subscribed_articles'),
    path('articles/create/', web_views.article_create, name='article_create'),
    path('articles/<int:pk>/', web_views.article_detail, name='article_detail'),
    path('articles/<int:pk>/edit/', web_views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', web_views.article_delete, name='article_delete'),
    path('articles/<int:pk>/approve/', web_views.approve_article, name='approve_article'),

    # Web interface routes - Newsletters
    path('newsletters/', web_views.newsletter_list, name='newsletter_list'),
    path('newsletters/create/', web_views.newsletter_create, name='newsletter_create'),
    path('newsletters/<int:pk>/', web_views.newsletter_detail, name='newsletter_detail'),
    path('newsletters/<int:pk>/edit/', web_views.newsletter_edit, name='newsletter_edit'),
    path('newsletters/<int:pk>/delete/', web_views.newsletter_delete, name='newsletter_delete'),

    # Web interface routes - Publishers
    path('publishers/', web_views.publisher_list, name='publisher_list'),
    path('publishers/<int:pk>/', web_views.publisher_detail, name='publisher_detail'),
    path('publishers/<int:pk>/subscribe/', web_views.subscribe_publisher, name='subscribe_publisher'),
    path('publishers/<int:pk>/unsubscribe/', web_views.unsubscribe_publisher, name='unsubscribe_publisher'),

    # Web interface routes - Subscriptions
    path('subscriptions/', web_views.my_subscriptions, name='my_subscriptions'),
    path('journalists/<int:pk>/subscribe/', web_views.subscribe_journalist, name='subscribe_journalist'),
    path('journalists/<int:pk>/unsubscribe/', web_views.unsubscribe_journalist, name='unsubscribe_journalist'),

    # API endpoints
    path('api/', include(router.urls)),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
