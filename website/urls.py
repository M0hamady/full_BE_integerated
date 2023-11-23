# urls.py

from django.urls import path
from .views import EmployeeUploadView, EmployeeWebsiteListCreateView, EmployeeWebsiteRetrieveUpdateDestroyView, PicListAPIView, PicUploadView

urlpatterns = [
    path('employees/', EmployeeWebsiteListCreateView.as_view(), name='employee-website-list-create'),
     path('employees/<uuid:pk>/', EmployeeWebsiteRetrieveUpdateDestroyView.as_view(), name='employee-website-retrieve-update-destroy'),
     path('pics/', PicListAPIView.as_view(), name='pic-list'),
     path('upload/pics/', PicUploadView.as_view(), name='upload-pic'),
     path('upload/employee/', EmployeeUploadView.as_view(), name='employee'),
]