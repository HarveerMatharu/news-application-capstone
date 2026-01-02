"""
Serializers for the news application API.

These serializers handle conversion between model instances and JSON format
for the REST API.
"""

from rest_framework import serializers
from .models import Article, Newsletter, Publisher, User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        """Meta options for UserSerializer."""

        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['id']


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for Publisher model."""

    class Meta:
        """Meta options for PublisherSerializer."""

        model = Publisher
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""

    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    publisher_id = serializers.IntegerField(
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        """Meta options for ArticleSerializer."""

        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'author_id',
            'publisher',
            'publisher_id',
            'created_at',
            'updated_at',
            'approved'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def create(self, validated_data):
        """
        Set author to current user on creation.

        Args:
            validated_data: Validated data from the request

        Returns:
            Article: The created article instance
        """
        validated_data['author'] = self.context['request'].user
        validated_data.pop('author_id', None)
        return super().create(validated_data)


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for Newsletter model."""

    author = UserSerializer(read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)
    article_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        """Meta options for NewsletterSerializer."""

        model = Newsletter
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'author',
            'articles',
            'article_ids'
        ]
        read_only_fields = ['id', 'created_at', 'author']

    def create(self, validated_data):
        """
        Set author to current user and handle articles.

        Args:
            validated_data: Validated data from the request

        Returns:
            Newsletter: The created newsletter instance
        """
        article_ids = validated_data.pop('article_ids', [])
        validated_data['author'] = self.context['request'].user

        newsletter = super().create(validated_data)

        if article_ids:
            newsletter.articles.set(article_ids)

        return newsletter

    def update(self, instance, validated_data):
        """
        Handle article updates.

        Args:
            instance: The newsletter instance to update
            validated_data: Validated data from the request

        Returns:
            Newsletter: The updated newsletter instance
        """
        article_ids = validated_data.pop('article_ids', None)

        instance = super().update(instance, validated_data)

        if article_ids is not None:
            instance.articles.set(article_ids)

        return instance
