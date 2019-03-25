from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsAdminOrOwnerPermission
from users.serializers import UserSerializer


def _get_user(request):
    return request.user


class OwnedModelViewSet(ModelViewSet):
    queryset_class = None
    queryset_ordered_by = None
    permission_classes = (IsAdminOrOwnerPermission,)

    def perform_update(self, serializer):
        current_user = _get_user(self.request)
        assert current_user.is_authenticated

        if current_user.is_staff:
            serializer.save()
        else:
            serializer.save(owner=current_user)

    def perform_create(self, serializer):
        self.perform_update(serializer)

    def get_queryset(self):
        current_user = _get_user(self.request)
        all_objects = self.queryset_class.objects.all()

        if self.queryset_ordered_by is not None:
            all_objects.order_by(self.queryset_ordered_by)

        if current_user.is_staff:
            return all_objects
        else:
            return all_objects.filter(owner=current_user)


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'patch', 'delete', 'options', 'head']

    def get_queryset(self):
        current_user = _get_user(self.request)
        all_users = User.objects.all().order_by('-date_joined')

        if current_user.is_staff:
            return all_users
        else:
            return all_users.filter(id=current_user.id)
