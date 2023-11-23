from django.urls import path
from.views import ProfileView, check_viewer_uuid

urlpatterns = [
    path('viewer/<uuid:uuid>/', check_viewer_uuid, name='check_viewer_uuid'),
    path('viewer/dash', ProfileView.as_view(), name='viewer_dash'),
]