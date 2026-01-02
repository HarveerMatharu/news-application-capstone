"""
Models for the news application.

This module contains all database models including User, Publisher,
Article, and Newsletter models with their associated signals.
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Custom user model with role-based fields."""

    ROLE_CHOICES = [
        ('READER', 'Reader'),
        ('EDITOR', 'Editor'),
        ('JOURNALIST', 'Journalist'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='READER'
    )

    # Reader-specific fields (ManyToMany)
    subscribed_publishers = models.ManyToManyField(
        'Publisher',
        related_name='subscribers',
        blank=True
    )
    subscribed_journalists = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='journalist_subscribers',
        blank=True,
        limit_choices_to={'role': 'JOURNALIST'}
    )

    def save(self, *args, **kwargs):
        """Override save to handle role-based field logic."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Assign to appropriate group based on role
        if is_new:
            self.assign_to_group()

    def assign_to_group(self):
        """Assign user to group based on role."""
        # Remove from all groups first
        self.groups.clear()

        # Add to appropriate group
        group_name = self.role.capitalize()
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)

    def __str__(self):
        """Return string representation of user."""
        return f"{self.username} ({self.role})"


class Publisher(models.Model):
    """Publisher model representing news organizations."""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    editors = models.ManyToManyField(
        User,
        related_name='publisher_editor_for',
        limit_choices_to={'role': 'EDITOR'},
        blank=True
    )
    journalists = models.ManyToManyField(
        User,
        related_name='publisher_journalist_for',
        limit_choices_to={'role': 'JOURNALIST'},
        blank=True
    )

    def __str__(self):
        """Return string representation of publisher."""
        return self.name

    class Meta:
        """Meta options for Publisher model."""

        ordering = ['-created_at']


class Article(models.Model):
    """Article model for news content."""

    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        limit_choices_to={'role': 'JOURNALIST'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    # Optional publisher (null for independent articles)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )

    def __str__(self):
        """Return string representation of article."""
        return f"{self.title} by {self.author.username}"

    class Meta:
        """Meta options for Article model."""

        ordering = ['-created_at']
        permissions = [
            ("approve_article", "Can approve article"),
        ]


class Newsletter(models.Model):
    """Newsletter model - curated collection of articles."""

    title = models.CharField(max_length=300)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='newsletters',
        limit_choices_to={'role__in': ['JOURNALIST', 'EDITOR']}
    )

    # Many-to-many relationship with articles
    articles = models.ManyToManyField(
        Article,
        related_name='newsletters',
        blank=True
    )

    def __str__(self):
        """Return string representation of newsletter."""
        return f"{self.title} by {self.author.username}"

    class Meta:
        """Meta options for Newsletter model."""

        ordering = ['-created_at']


# Signal handlers for article approval
@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
    """
    Signal handler for article approval.

    Sends email notifications and posts to X (Twitter) when approved.

    Args:
        sender: The model class (Article)
        instance: The actual Article instance
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    # Only trigger if article was just approved (not on creation)
    if not created and instance.approved:
        from .tasks import send_article_notifications, post_to_twitter

        # Send email notifications to subscribers
        send_article_notifications(instance)

        # Post to X (Twitter)
        post_to_twitter(instance)


@receiver(post_save, sender=User)
def create_user_groups(sender, instance, created, **kwargs):
    """
    Create default groups with permissions if they don't exist.

    Args:
        sender: The model class (User)
        instance: The actual User instance
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    if created:
        # Create groups with permissions
        setup_groups_and_permissions()


def setup_groups_and_permissions():
    """Setup default groups and their permissions."""
    # Get content types
    article_ct = ContentType.objects.get_for_model(Article)
    newsletter_ct = ContentType.objects.get_for_model(Newsletter)

    # Reader Group
    reader_group, _ = Group.objects.get_or_create(name='Reader')
    reader_perms = [
        Permission.objects.get(
            codename='view_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='view_newsletter',
            content_type=newsletter_ct
        ),
    ]
    reader_group.permissions.set(reader_perms)

    # Editor Group
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    editor_perms = [
        Permission.objects.get(
            codename='view_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='change_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='delete_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='approve_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='view_newsletter',
            content_type=newsletter_ct
        ),
        Permission.objects.get(
            codename='change_newsletter',
            content_type=newsletter_ct
        ),
        Permission.objects.get(
            codename='delete_newsletter',
            content_type=newsletter_ct
        ),
    ]
    editor_group.permissions.set(editor_perms)

    # Journalist Group
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')
    journalist_perms = [
        Permission.objects.get(
            codename='add_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='view_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='change_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='delete_article',
            content_type=article_ct
        ),
        Permission.objects.get(
            codename='add_newsletter',
            content_type=newsletter_ct
        ),
        Permission.objects.get(
            codename='view_newsletter',
            content_type=newsletter_ct
        ),
        Permission.objects.get(
            codename='change_newsletter',
            content_type=newsletter_ct
        ),
        Permission.objects.get(
            codename='delete_newsletter',
            content_type=newsletter_ct
        ),
    ]
    journalist_group.permissions.set(journalist_perms)
