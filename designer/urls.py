from django.urls import path

from .views import AssignDesignersAPIView, DesignerListAPIView, webhook

urlpatterns = [
    path('all/<uuid:technical_uuid>/', DesignerListAPIView.as_view(), name='all_designers'),
    path('update/<uuid:uuid>/<uuid:technical_uuid>', AssignDesignersAPIView.as_view(), name='update_designers'),
    path('webhook/', webhook, name='webhook'),
]