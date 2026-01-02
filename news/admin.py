"""
Django admin configuration for the news application.

This module configures the admin interface for User, Publisher, Article,
and Newsletter models with custom actions and displays.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Article, Newsletter, Publisher


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with role management."""

    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
        (
            'Subscriptions',
            {
                'fields': (
                    'subscribed_publishers',
                    'subscribed_journalists'
                )
            }
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Publisher admin with relationship management."""

    list_display = ['name', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['editors', 'journalists']
    readonly_fields = ['created_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin with approval functionality."""

    list_display = [
        'title',
        'author',
        'publisher',
        'approved',
        'created_at'
    ]
    list_filter = ['approved', 'created_at', 'publisher']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']

    actions = ['approve_articles']

    def approve_articles(self, request, queryset):
        """
        Bulk approve articles action.

        Args:
            request: The HTTP request object
            queryset: QuerySet of selected articles
        """
        count = queryset.filter(approved=False).update(approved=True)
        self.message_user(
            request,
            f'{count} articles approved successfully.'
        )

    approve_articles.short_description = "Approve selected articles"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Newsletter admin with article management."""

    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'description']
    filter_horizontal = ['articles']
    readonly_fields = ['created_at']
