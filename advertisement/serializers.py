from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from advertisement.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('title', 'description', 'image')


class TagValueSerializer(ModelSerializer):
    fields = ('tag', 'value')


class AdvertisementSerializer(ModelSerializer):
    company = StringRelatedField()
    tags = TagValueSerializer(many=True)

    class Meta:
        fields = ('url', 'title', 'description', 'remaining_days', 'company', 'tags')
