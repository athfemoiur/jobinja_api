from django.urls import path

from advertisement.views import AdvertisementListView, CompanyListView

app_name = 'advertisement'

urlpatterns = [
    path('advertisements/', AdvertisementListView.as_view(), name='advertisement-list'),
    path('companeis/', CompanyListView.as_view(), name='company-list')
]
