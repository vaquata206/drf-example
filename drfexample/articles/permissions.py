from rest_framework import permissions
from .models import Article


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Article):
            return obj.author == request.user
        else:
            return False
