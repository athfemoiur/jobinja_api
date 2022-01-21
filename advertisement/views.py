from rest_framework.generics import ListAPIView

from advertisement.models import Advertisement, Company
from advertisement.serializers import AdvertisementSerializer, CompanySerializer


class AdvertisementListView(ListAPIView):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all().prefetch_related('tags').select_related('company')


class CompanyListView(ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
