import json
from json import JSONDecodeError

from rest_framework.serializers import HyperlinkedModelSerializer, \
    ValidationError

from modules.models import Function, Module


class FunctionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Function
        fields = ('id', 'url', 'name', 'module', 'options')

    def validate_options(self, value):
        try:
            json.loads(value)
        except JSONDecodeError:
            raise ValidationError('Not a valid JSON text.')

        try:
            assert type(json.loads(value)) is list
        except AssertionError:
            raise ValidationError('Should be a list.')

        return value


class ChildFunctionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Function
        fields = ('id', 'url', 'name', 'options')


class ModuleSerializer(HyperlinkedModelSerializer):
    functions = ChildFunctionSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'url', 'name', 'repo', 'functions',
                  'input_schema', 'output_schema')
        read_only_fields = ('functions',)

    def validate_input_schema(self, value):
        try:
            json.loads(value)
        except JSONDecodeError:
            raise ValidationError('Not a valid JSON text.')

        return value

    def validate_output_schema(self, value):
        return self.validate_input_schema(value)
