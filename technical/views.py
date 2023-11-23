from datetime import datetime
from django.shortcuts import render
from client.models import Client
from client.serializers import ClientSerializer
from project.models import Project, ProjectBasic
from project.serializers import BasicProjectSerializer, ProjectSerializer_client
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from technical.models import Technical
from technical.serializers import TechSerializer

# Create your views here.

@api_view(['GET'])
def check_tech_uuid(request, uuid):
    try:
        viewer = Technical.objects.get(uuid=uuid)
    except Technical.DoesNotExist:
        return Response({'error': 'Technical not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TechSerializer(viewer)
    return Response(serializer.data)
@api_view(['GET'])
def technical_client(request, technical_uuid):
    try:
        technical = Technical.objects.get(uuid=technical_uuid)
    except:return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)
    
    clients = Client.objects.all()
    res = []
    for client in clients:
        if client.calculate_data_completion_percentage <= 90:
            res.append(client)

    client_data = [{'id': client.id,
                     'name': client.name,
                     'created_date': client.created_date,
                     'number': client.number,
                     'location': client.location,
                     'locationLink': client.locationLink,
                     'coming_from': client.coming_from,
                     'uuid': client.uuid,
                     'is_active': client.is_active,
                     'is_viewer_viewed': client.is_viewer_viewed,
                     'date_viewer_viewed': client.date_viewer_viewed,
                     'is_tech_viewed': client.is_tech_viewed,
                     'date_tech_viewed': client.date_tech_viewed,
                     'meeting_time': client.meeting_time,
                     'contract_meeting_time': client.contract_meeting_time,
                     'is_meeting_approved': client.is_meeting_approved,
                     'is_contract_meeting_approved': client.is_contract_meeting_approved,
                     'is_location_approved': client.is_location_approved,
                     'is_contract_location_approved': client.is_contract_location_approved,
                     'is_3d_design_approved': client.is_3d_design_approved,
                     'is_client_project_finished': client.is_client_project_finished,
                     'is_Project_done': client.is_Project_done,
                     'percentage': int(client.calculate_data_completion_percentage),
                     } for client in res]
    res_need_actions = []
    for client in clients:
        if not client.is_tech_viewed:
            res_need_actions.append(client)

    client_data_need_actions = [{'id': client.id,
                     'name': client.name,
                     'created_date': client.created_date,
                     'number': client.number,
                     'location': client.location,
                     'locationLink': client.locationLink,
                     'coming_from': client.coming_from,
                     'uuid': client.uuid,
                     'is_active': client.is_active,
                     'is_viewer_viewed': client.is_viewer_viewed,
                     'date_viewer_viewed': client.date_viewer_viewed,
                     'is_tech_viewed': client.is_tech_viewed,
                     'date_tech_viewed': client.date_tech_viewed,
                     'meeting_time': client.meeting_time,
                     'contract_meeting_time': client.contract_meeting_time,
                     'is_meeting_approved': client.is_meeting_approved,
                     'is_contract_meeting_approved': client.is_contract_meeting_approved,
                     'is_location_approved': client.is_location_approved,
                     'is_contract_location_approved': client.is_contract_location_approved,
                     'is_3d_design_approved': client.is_3d_design_approved,
                     'is_client_project_finished': client.is_client_project_finished,
                     'is_Project_done': client.is_Project_done,
                     'percentage': int(client.calculate_data_completion_percentage),
                     } for client in res_need_actions]
    res_approved = [] # current clients 
    for client in clients:
        if client.is_contract_approved:
            res_approved.append(client)

    client_data_approved = [{'id': client.id,
                     'name': client.name,
                     'created_date': client.created_date,
                     'number': client.number,
                     'location': client.location,
                     'locationLink': client.locationLink,
                     'coming_from': client.coming_from,
                     'uuid': client.uuid,
                     'is_active': client.is_active,
                     'is_viewer_viewed': client.is_viewer_viewed,
                     'date_viewer_viewed': client.date_viewer_viewed,
                     'is_tech_viewed': client.is_tech_viewed,
                     'date_tech_viewed': client.date_tech_viewed,
                     'meeting_time': client.meeting_time,
                     'contract_meeting_time': client.contract_meeting_time,
                     'is_meeting_approved': client.is_meeting_approved,
                     'is_contract_meeting_approved': client.is_contract_meeting_approved,
                     'is_location_approved': client.is_location_approved,
                     'is_contract_location_approved': client.is_contract_location_approved,
                     'is_3d_design_approved': client.is_3d_design_approved,
                     'is_client_project_finished': client.is_client_project_finished,
                     'is_Project_done': client.is_Project_done,
                     'percentage': int(client.calculate_data_completion_percentage),
                     } for client in res_approved]

    
    clients_unseen = Client.objects.filter(is_tech_viewed = False)
    clients_seen = Client.objects.filter(is_tech_viewed = True)

    serializer_seen =ClientSerializer(clients_seen,many=True)
    serializer_unseen =ClientSerializer(clients_unseen,many=True)
    context = {
        # "from_viewer_team":serializer_seen.data,
        "from_viewer_team": {
            "client_recently_added":len(client_data_need_actions),
            'clients': client_data,"needs_action":client_data_need_actions,'current_clients':client_data_approved

        }, # its bercentage is more than 25% 
        "from_designers":"client updated by designers", #
        "todays_meetings":"todays meting" # list of clients name and date with branch name
    }
    
    return Response(context, status=status.HTTP_200_OK)
@api_view(['GET'])
def technical_client_today_meetings(request, technical_uuid):
    try:
        technical = Technical.objects.get(uuid=technical_uuid)
    except:return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    current_datetime = datetime.now()
    print(current_datetime.date())
    clients_Contract_meeting_approved = Client.objects.filter(is_contract_meeting_approved=True,contract_meeting_time__date =current_datetime.date() )
    clients_Contract_meeting_unapproved = Client.objects.filter(is_contract_meeting_approved=False,contract_meeting_time__date =current_datetime.date() )

    serializer_seen =ClientSerializer(clients_Contract_meeting_approved,many=True)
    serializer_unseen =ClientSerializer(clients_Contract_meeting_unapproved,many=True)
    context = {
        # waiting for cancel status to add
        "clients_today_meetings_approved":serializer_seen.data,
        "clients_today_meetings_waiting":serializer_unseen.data,
    }
    
    return Response(context, status=status.HTTP_200_OK)
@api_view(['GET'])     
def technical_client_data(request, technical_uuid):
    try:
        technical = Technical.objects.get(uuid=technical_uuid)
    except:return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        client_uuid = request.data['client_uuid']
        client = Client.objects.get(uuid = client_uuid)
    except:return Response({'error': 'Invalid client_uuid please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        project = Project.objects.get(client  = client)
    except:return Response({'error': 'client has no project yet'}, status=status.HTTP_400_BAD_REQUEST)
    client_project = ProjectSerializer_client(project).data  

    try: 
        project_basic = ProjectBasic.objects.get(project  = project)
    except:return Response({'error': 'client has no project yet'}, status=status.HTTP_400_BAD_REQUEST)
    client_project_basic_data = BasicProjectSerializer(project_basic).data  
    context = {
        # client basic_data
        "client_project":client_project,
        "client_project_basic":client_project_basic_data,
    }
    
    return Response(context, status=status.HTTP_200_OK)
     