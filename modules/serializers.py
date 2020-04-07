import json
from json import JSONDecodeError

from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError

from mlsploit import Module as ModuleConfig
from mlsploit.core.module import Option as OptionConfig, Tag as TagConfig

from modules.models import Function, Module


class FunctionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Function
        fields = (
            "id",
            "url",
            "name",
            "module",
            "doctxt",
            "options",
            "creates_new_files",
            "modifies_input_files",
            "expected_filetype",
            "optional_filetypes",
            "output_tags",
        )

    def validate_options(self, value):
        raw_options = json.loads(value)
        valid_options = map(lambda d: OptionConfig(**d), raw_options)
        valid_options = map(lambda o: o.dict(), valid_options)
        return json.dumps(list(valid_options))

    def validate_optional_filetypes(self, value):
        value = json.loads(value)
        if not isinstance(value, list):
            raise ValidationError("Should be a list")
        return json.dumps(value)

    def validate_output_tags(self, value):
        raw_tags = json.loads(value)
        valid_tags = map(lambda d: TagConfig(**d), raw_tags)
        valid_tags = map(lambda t: t.dict(), valid_tags)
        return json.dumps(list(valid_tags))


class ChildFunctionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Function
        fields = (
            "id",
            "url",
            "name",
            "module",
            "doctxt",
            "options",
            "creates_new_files",
            "modifies_input_files",
            "expected_filetype",
            "optional_filetypes",
            "output_tags",
        )


class ModuleSerializer(HyperlinkedModelSerializer):
    functions = ChildFunctionSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = (
            "id",
            "url",
            "name",
            "repo_url",
            "repo_branch",
            "display_name",
            "functions",
            "tagline",
            "doctxt",
            "config",
            "icon_url",
        )
        read_only_fields = ("functions",)

    def validate_config(self, value):
        valid_config = ModuleConfig.deserialize(value)
        return valid_config.serialize()
