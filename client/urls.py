from django.urls import path
from .views import AddClientActionView, ClientByUUIDView, ClientProjectUpdateView, ClientRegistrationAPIView, ClientRegistrationView, ContactUsView, client_data, client_retrieve_view, get_all_clients,  client_create_view, get_all_clients_viewer, get_all_clients_viewer_today_meetings, get_all_projects, get_client, index, update_client

urlpatterns = [
    # path('', index, name='client'),
    # path('clients/<uuid:marketing_uuid>/', update_basic_project, name='client-list'),
    path('clients/all/<uuid:marketing_uuid>/',  get_all_clients, name='client-list'),
    path('clients/all/viewer/<uuid:viewer_uuid>/',  get_all_clients_viewer, name='client-list-viewer'),
    path('clients/all/viewer/projects/<uuid:viewer_uuid>/', get_all_projects, name='client-list-viewer-projects'),
    path('clients/all/viewer/meetings/<uuid:viewer_uuid>/',  get_all_clients_viewer_today_meetings, name='client-list-viewer'),
    # path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/create/<uuid:viewer_uuid>/', client_create_view, name='client-create'),
    path('clients/get/<uuid:viewer_uuid>/', get_client, name='client-get'),
    path('client/<uuid:marketing_uuid>/', client_retrieve_view, name='client-retrieve'),
    path('clients/<uuid:viewer_uuid>/update/', update_client, name='client-update'),
    # site apis
    path('api/clients/check/<uuid:uuid>/', ClientByUUIDView.as_view(), name='client-by-uuid'),
    path('api/clients/register/', ClientRegistrationView.as_view(), name='client-registration'),
    path('api/clients/info/<uuid:client_uuid>/', client_data, name='client-registration'),
    path('api/register-client/', ClientRegistrationAPIView.as_view(), name='register-client'),
    path('api/clients/pics/<uuid:client_uuid>/', client_data, name='client-registration'),
    # get client info >> road map
    # get project pics
    # get payments
    path('api/contact/', ContactUsView.as_view(), name='contact-api'),
    path('add_client_action/<int:client_id>/', AddClientActionView, name='add_client_action'),
    path('client/update/self/<uuid:uuid>/', ClientProjectUpdateView.as_view(), name='client_project_update_self'),

]
# 010056529