import json
import os

from rest_framework.serializers import FileField, \
    SerializerMethodField, ValidationError

from api.settings import MEDIA_DIR, MEDIA_URL
from files.models import File
from users.serializers import OwnedHyperlinkedModelSerializer


class FileSerializer(OwnedHyperlinkedModelSerializer):
    blob = FileField(write_only=True)
    blob_url = SerializerMethodField('make_blob_url')

    class Meta:
        model = File
        fields = ('id', 'url', 'name', 'owner',
                  'blob', 'blob_url', 'kind',
                  'tags', 'parent_file',
                  'modified_versions',
                  'date_uploaded')
        read_only_fields = ('owner', 'kind',
                            'parent_file',
                            'modified_versions',
                            'date_uploaded')

    def make_blob_url(self, obj):
        print(MEDIA_DIR, obj.blob.path)
        blob_url = os.path.relpath(obj.blob.path, MEDIA_DIR)

        if 'request' in self.context:
            root_url = self.context['request'].build_absolute_uri('/')
            blob_url = '/'.join(
                p.strip('/') for p in (root_url, MEDIA_URL, blob_url))

        return blob_url

    def validate_blob(self, value):
        if 'request' not in self.context:
            raise ValidationError('Cannot validate without request.')

        current_user = getattr(self.context['request'], 'user', None)

        if not current_user:
            raise ValidationError('Cannot validate without logged in user.')

        filename = value.name

        existing_files_for_user = File.objects.filter(
            owner__id=current_user.id, name=filename)

        if len(existing_files_for_user) > 0:
            raise ValidationError(
                f'File \'{filename}\' already exists '
                f'for {current_user.username}.')

        return value

    def validate_tags(self, value):
        if not value:
            value = "{}"

        try:
            json.loads(value)
        except json.decoder.JSONDecodeError:
            raise ValidationError('Unable to decode.')

        return value




class ForAdminFileSerializer(FileSerializer):
    class Meta:
        model = File
        fields = ('id', 'url', 'name', 'owner',
                  'blob', 'blob_url', 'kind',
                  'tags', 'parent_file',
                  'date_uploaded')
        read_only_fields = ('modified_versions', 'date_uploaded')
