from files.models import File
from files.serializers import FileSerializer, ForAdminFileSerializer
from users.permissions import CanDeleteFilePermission
from users.views import OwnedModelViewSet


class FileViewSet(OwnedModelViewSet):
    """
    list: Shows all the files belonging to the authenticated user.

    create: Creates a new file for the authenticated user.

    read: Shows the details for the requested file
    if it is owned by the authenticated user.

    update: Only an administrator can update the file details
    once it is uploaded by the user.

    partial_update: Only an administrator can update the file details
    once it is uploaded by the user.

    delete: Deletes the file if it is of the 'INPUT' kind,
    and is owned by the authenticated user.
    The file cannot be deleted if it is associated with any run
    (user will have to delete the associated runs first).
    """
    queryset_class = File
    queryset_ordered_by = '-date_uploaded'
    filter_fields = ('owner', 'kind')
    permission_classes = OwnedModelViewSet.permission_classes \
                         + (CanDeleteFilePermission,)

    def get_serializer_class(self):
        if self.request and self.request.user.is_staff:
            return ForAdminFileSerializer

        return FileSerializer
