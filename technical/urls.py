from django.urls import path
from .views import *
urlpatterns = [
    path('all-clients/<uuid:technical_uuid>/', technical_client, name='technical_clients'),
    path('today-meetings/<uuid:technical_uuid>/', technical_client_today_meetings, name='technical_client_today_meetings'),
    path('client-data/<uuid:technical_uuid>/', technical_client_data, name='technical_client_data'),
    path('is_technical/<uuid:uuid>/', check_tech_uuid, name='check_technical_uuid'),

]