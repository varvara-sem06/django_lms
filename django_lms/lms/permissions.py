from rest_framework.permissions import BasePermission


class IsModeratorOrOwner(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_moderator = request.user.groups.filter(name="Moderators").exists()

        if request.method == "POST" and is_moderator:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        is_moderator = request.user.groups.filter(name="Moderators").exists()

        if is_moderator:
            return request.method in (
                "GET",
                "HEAD",
                "OPTIONS",
                "PUT",
                "PATCH",
            )

        return obj.owner == request.user
