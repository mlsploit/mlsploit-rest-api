import json
from json import JSONDecodeError

from rest_framework.serializers import HyperlinkedRelatedField, ValidationError

from files.models import File
from pipelines.models import Pipeline, Task, Run, Job
from users.serializers import OwnedHyperlinkedModelSerializer, \
    get_owned_hyperlinked_related_field


def get_owned_hyperlinked_related_files_field_for_run(
        *attr_args, **attr_kwargs):

    class OwnedHyperlinkedRelatedFilesField(HyperlinkedRelatedField):
        def get_queryset(self):
            current_user = self.context['request'].user

            queryset = File.objects.filter(owner__id=current_user.id)
            queryset = queryset.filter(kind=File.FileKind.INPUT.value)

            return queryset

    return OwnedHyperlinkedRelatedFilesField(*attr_args, **attr_kwargs)


class JobSerializer(OwnedHyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'url', 'owner', 'run', 'task', 'parent_job',
                  'status', 'output', 'output_files', 'logs',
                  'date_created')
        read_only_fields = ('owner', 'run', 'task',
                            'parent_job', 'date_created')

    def validate_output_files(self, value):
        try:
            for output_file in value:
                assert output_file.kind == File.FileKind.OUTPUT.value
        except AssertionError:
            raise ValidationError('Output file is not \'OUTPUT\' kind.')

        try:
            for output_file in value:
                assert output_file.owner.id == self.instance.owner.id
        except AssertionError:
            raise ValidationError('Job owner does not own the output file')

        return value


class RunSerializer(OwnedHyperlinkedModelSerializer):
    pipeline = get_owned_hyperlinked_related_field(
        Pipeline, view_name='pipeline-detail')

    files = get_owned_hyperlinked_related_files_field_for_run(
        view_name='file-detail', many=True)

    class Meta:
        model = Run
        fields = ('id', 'url', 'owner', 'pipeline',
                  'files', 'jobs', 'date_created')
        read_only_fields = ('owner', 'jobs', 'date_created')

    def validate_pipeline(self, value):
        try:
            assert value.enabled
        except AssertionError:
            raise ValidationError(f'Pipeline \'{value.name}\' is not enabled.')

        return value


class TaskSerializer(OwnedHyperlinkedModelSerializer):
    pipeline = get_owned_hyperlinked_related_field(
        Pipeline, view_name='pipeline-detail')

    class Meta:
        model = Task
        fields = ('id', 'url', 'owner', 'pipeline',
                  'function', 'arguments', 'order',
                  'date_created')
        read_only_fields = ('owner', 'order', 'date_created')

    def validate_function(self, value):
        if value is None:
            raise ValidationError(f'Function may not be empty.')

        return value

    def validate_arguments(self, value):
        try:
            json.loads(value)
        except JSONDecodeError:
            raise ValidationError('Not a valid JSON text.')

        return value

    def validate(self, data):
        data = super(TaskSerializer, self).validate(data)

        # TODO: validate arguments with `function.options` here.

        return data


class ChildTaskSerializer(OwnedHyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'url', 'function', 'arguments', 'order')
        

class PipelineSerializer(OwnedHyperlinkedModelSerializer):
    tasks = ChildTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Pipeline
        fields = ('id', 'url', 'name', 'owner',
                  'tasks', 'runs', 'enabled', 'date_created')
        read_only_fields = ('owner', 'tasks', 'runs', 'date_created')
