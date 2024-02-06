from django.urls import path
from .views import *
urlpatterns = [
    path('all-clients/<uuid:technical_uuid>/', technical_client, name='technical_clients'),
    path('today-meetings/<uuid:technical_uuid>/', technical_client_today_meetings, name='technical_client_today_meetings'),
    path('client-data/<uuid:technical_uuid>/', technical_client_data, name='technical_client_data'),
    path('is_technical/<uuid:uuid>/', check_tech_uuid, name='check_technical_uuid'),
    path('create_project-ai/<int:project_id>/', CustomerServicesView.as_view(), name='create_project_ai'),
    path('create_project-ai/steps/<int:project_id>/<int:floor_id>/', CustomerServicesStepsView.as_view(), name='create_project_ai_step'),
    path('add_step_to_floor/<int:client_id>/<int:step_id>/', add_step_to_floor, name='add_step_to_floor'),
]