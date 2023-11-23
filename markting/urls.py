from django.urls import path

from markting.views import checkLicenseMarkting

urlpatterns = [
    path('check/<uuid:markting_uuid>/', checkLicenseMarkting, name='checkLicenseMarkting'),
]