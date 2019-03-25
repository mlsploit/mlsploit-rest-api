from pipelines.models import Pipeline, Task, Run, Job
from pipelines.serializers import PipelineSerializer, TaskSerializer, \
    RunSerializer, JobSerializer
from users.permissions import IsAdminOrSafeMethodPermission
from users.views import OwnedModelViewSet


class JobViewSet(OwnedModelViewSet):
    """
    API endpoint that allows pipelines to be viewed or edited.
    """
    queryset_class = Job
    queryset_ordered_by = '-date_created'
    serializer_class = JobSerializer
    filter_fields = ('run', 'status')
    http_method_names = ['get', 'put', 'patch', 'options', 'head']
    permission_classes = OwnedModelViewSet.permission_classes \
                         + (IsAdminOrSafeMethodPermission,)


class RunViewSet(OwnedModelViewSet):
    """
    API endpoint that allows pipelines to be viewed or edited.
    """
    queryset_class = Run
    queryset_ordered_by = '-date_created'
    serializer_class = RunSerializer
    filter_fields = ('pipeline',)
    http_method_names = ['get', 'post', 'delete', 'options', 'head']


class TaskViewSet(OwnedModelViewSet):
    """
    API endpoint that allows pipelines to be viewed or edited.
    """
    queryset_class = Task
    queryset_ordered_by = 'order'
    serializer_class = TaskSerializer
    filter_fields = ('pipeline',)
    http_method_names = ['get', 'post', 'options', 'head']


class PipelineViewSet(OwnedModelViewSet):
    """
    API endpoint that allows pipelines to be viewed or edited.
    """
    queryset_class = Pipeline
    queryset_ordered_by = '-date_created'
    serializer_class = PipelineSerializer
    filter_fields = ('owner',)
