"""
Management command to setup groups and permissions for the news application.

Run: python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Article, Newsletter


class Command(BaseCommand):
    """Command to setup user groups and permissions."""

    help = 'Setup user groups and permissions'

    def handle(self, *args, **options):
        """
        Execute the command to create groups and assign permissions.

        Args:
            *args: Variable length argument list
            **options: Arbitrary keyword arguments
        """
        self.stdout.write('Setting up groups and permissions...')

        # Get content types
        article_ct = ContentType.objects.get_for_model(Article)
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)

        # Reader Group
        reader_group, created = Group.objects.get_or_create(name='Reader')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created Reader group')
            )

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
        self.stdout.write(
            self.style.SUCCESS(
                f'  - Assigned {len(reader_perms)} permissions to Reader'
            )
        )

        # Editor Group
        editor_group, created = Group.objects.get_or_create(name='Editor')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created Editor group')
            )

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
        self.stdout.write(
            self.style.SUCCESS(
                f'  - Assigned {len(editor_perms)} permissions to Editor'
            )
        )

        # Journalist Group
        journalist_group, created = Group.objects.get_or_create(
            name='Journalist'
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created Journalist group')
            )

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
        self.stdout.write(
            self.style.SUCCESS(
                f'  - Assigned {len(journalist_perms)} permissions '
                f'to Journalist'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                '\nGroups and permissions setup complete!'
            )
        )
