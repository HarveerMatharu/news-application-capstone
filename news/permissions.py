"""
Custom permission classes for role-based access control.

These permissions are used in API views to restrict access based on user roles.
"""

from rest_framework import permissions


class IsJournalist(permissions.BasePermission):
    """
    Permission class to check if user is a Journalist.

    Only allows access if the authenticated user has the JOURNALIST role.
    """

    def has_permission(self, request, view):
        """
        Check if user has journalist role.

        Args:
            request: The HTTP request object
            view: The view being accessed

        Returns:
            bool: True if user is authenticated and is a journalist
        """
        return (
            request.user.is_authenticated and
            request.user.role == 'JOURNALIST'
        )


class IsEditor(permissions.BasePermission):
    """
    Permission class to check if user is an Editor.

    Only allows access if the authenticated user has the EDITOR role.
    """

    def has_permission(self, request, view):
        """
        Check if user has editor role.

        Args:
            request: The HTTP request object
            view: The view being accessed

        Returns:
            bool: True if user is authenticated and is an editor
        """
        return (
            request.user.is_authenticated and
            request.user.role == 'EDITOR'
        )


class IsEditorOrJournalist(permissions.BasePermission):
    """
    Permission class to check if user is either an Editor or Journalist.

    Allows access for both editors and journalists.
    """

    def has_permission(self, request, view):
        """
        Check if user has editor or journalist role.

        Args:
            request: The HTTP request object
            view: The view being accessed

        Returns:
            bool: True if user is authenticated and is editor or journalist
        """
        return (
            request.user.is_authenticated and
            request.user.role in ['EDITOR', 'JOURNALIST']
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    Read permissions are allowed for any request. Write permissions are
    only allowed to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user is the owner for write operations.

        Args:
            request: The HTTP request object
            view: The view being accessed
            obj: The object being accessed

        Returns:
            bool: True for read operations or if user is the owner
        """
        # Read permissions for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only to owner
        return obj.author == request.user


class IsReader(permissions.BasePermission):
    """
    Permission class to check if user is a Reader.

    Only allows access if the authenticated user has the READER role.
    """

    def has_permission(self, request, view):
        """
        Check if user has reader role.

        Args:
            request: The HTTP request object
            view: The view being accessed

        Returns:
            bool: True if user is authenticated and is a reader
        """
        return (
            request.user.is_authenticated and
            request.user.role == 'READER'
        )
