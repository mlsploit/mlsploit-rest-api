from rest_framework.permissions import BasePermission, SAFE_METHODS

from files.models import File
from pipelines.models import Run


class IsAdminOrOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner.id == request.user.id


class IsAdminOrSafeMethodPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff
            or (request.user.is_authenticated and request.method in SAFE_METHODS)
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (
            request.user.is_authenticated and request.method in SAFE_METHODS
        )


class CanDeleteFilePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            associated_runs = Run.objects.filter(files__id=obj.id)

            if len(associated_runs) > 0 or obj.kind == File.FileKind.OUTPUT.value:
                return False

        return True


class IsAdminOrCannotEditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (
            request.user.is_authenticated
            and request.method in SAFE_METHODS + ("POST", "DELETE")
        )
