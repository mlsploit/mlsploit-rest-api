from rest_framework.viewsets import ModelViewSet

from modules.models import Function, Module
from modules.serializers import FunctionSerializer, ModuleSerializer
from users.permissions import IsAdminOrSafeMethodPermission


class ModuleViewSet(ModelViewSet):
    """
    API endpoint that allows modules to be viewed or edited.
    """
    queryset = Module.objects.all().order_by('-id')
    serializer_class = ModuleSerializer
    permission_classes = (IsAdminOrSafeMethodPermission,)
    http_method_names = ['get', 'post', 'delete', 'options', 'head']


class FunctionViewSet(ModelViewSet):
    """
    API endpoint that allows functions to be viewed or edited.
    """
    queryset = Function.objects.all().order_by('-id')
    serializer_class = FunctionSerializer
    filter_fields = ('module',)
    permission_classes = (IsAdminOrSafeMethodPermission,)
    http_method_names = ['get', 'options', 'head']
