from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from advertisement.models import Company, Advertisement, TagValue


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('title', 'description', 'image')


class TagValueSerializer(ModelSerializer):
    tag = StringRelatedField()

    class Meta:
        model = TagValue
        fields = ('tag', 'value')


class AdvertisementSerializer(ModelSerializer):
    company = StringRelatedField()
    tag_values = TagValueSerializer(many=True)

    class Meta:
        model = Advertisement
        fields = ('url', 'title', 'description', 'remaining_days', 'company', 'tag_values')
