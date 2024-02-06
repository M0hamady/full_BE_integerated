from django.urls import path

from markting.views import CustomerServicesView, UpdateNotesView, checkLicenseMarkting, update_meeting_time

urlpatterns = [
    path('check/<uuid:markting_uuid>/', checkLicenseMarkting, name='checkLicenseMarkting'),
    path('CustomerServicesView', CustomerServicesView.as_view(), name='CustomerServicesView'),
    path('update_meeting_time/<int:client_id>/', update_meeting_time, name='update_meeting_time'),
    path('update_notes/<int:client_action_id>/', UpdateNotesView.as_view(), name='update_notes'),

]