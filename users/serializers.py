from rest_auth.models import TokenModel
from rest_framework.serializers import HyperlinkedModelSerializer, \
    ModelSerializer, HyperlinkedRelatedField, \
    SerializerMethodField, ValidationError

from users.models import User


class OwnedHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    def validate(self, data):
        data = super(OwnedHyperlinkedModelSerializer, self)\
            .validate(data)

        if 'request' not in self.context:
            raise ValidationError('Cannot validate without request.')

        current_user = getattr(self.context['request'], 'user', None)

        if not current_user:
            raise ValidationError('Cannot validate without logged in user.')

        if not current_user.is_staff:
            to_check_ownership = list()
            for field in data.values():
                if getattr(field, 'owner', None):
                    to_check_ownership.append(field)
                elif type(field) is list:
                    for field_item in field:
                        if getattr(field_item, 'owner', None):
                            to_check_ownership.append(field_item)

            for item in to_check_ownership:
                if current_user.id != item.owner.id:
                    raise ValidationError(
                        'Unauthorized request.')

        return data


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'files', 'pipelines')
        read_only_fields = ('files', 'pipelines')


class TokenSerializer(ModelSerializer):
    """
    Serializer for Token model.
    """

    token = SerializerMethodField()

    class Meta:
        model = TokenModel
        fields = ('token',)

    def get_token(self, obj):
        return obj.key


def get_owned_hyperlinked_related_field(
        primary_key_class, *attr_args, **attr_kwargs):

    class OwnedHyperlinkedRelatedField(HyperlinkedRelatedField):
        def get_queryset(self):
            current_user = self.context['request'].user
            queryset = primary_key_class.objects.filter(
                owner__id=current_user.id)

            return queryset

    return OwnedHyperlinkedRelatedField(*attr_args, **attr_kwargs)
