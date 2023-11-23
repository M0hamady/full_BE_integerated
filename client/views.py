from datetime import datetime
from django.shortcuts import render
from markting.models import Marketing
from project.models import Project, ProjectBasic
from project.serializers import BasicProjectSerializer, ProjectSerializer, ProjectSerializer_client
from rest_framework.response import Response
from django.db.models import Case, F, FloatField, When
from django.db.models.functions import Cast
# Create your views here.
from rest_framework import generics, status
from supportconstruction import settings
from teamview.models import Viewer
from technical.models import Technical
from .models import Client, Contact
from .serializers import ClientAPI, ClientRegistrationSerializer, ClientSerializer, ClientUpdateSerializer, ClientWebSerializer, ContactSerializer
from rest_framework.views import APIView


from rest_framework.decorators import api_view

def index(request):
    return render(request, 'index.html')
@api_view(['PUT'])
def update_client(request, viewer_uuid):
    try:
        viewer = Viewer.objects.get(uuid=viewer_uuid)
    except :
        try:
            markting = Marketing.objects.get(uuid=viewer_uuid)
        except:
            try:
                technical = Technical.objects.get(uuid=viewer_uuid)
            except:return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        client_uuid = request.data.get('client_uuid')
        client = Client.objects.get(uuid=client_uuid)
    except Client.DoesNotExist:
        return Response({'error': 'Invalid client_uuid'}, status=status.HTTP_400_BAD_REQUEST)
    print(client)
    client_data = request.data.dict() 
    for key, value in client_data.items():
            if hasattr(client, key):
                setattr(client, key, value)
    client.save()
    serializer = ClientUpdateSerializer(client)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_client(request, viewer_uuid):
    try:
        viewer = Marketing.objects.get(uuid=viewer_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Invalid secret key, please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        try:
            client_uuid = request.data.get('client_uuid')
        except :
            return Response({'error': 'add client_uuid to body'}, status=status.HTTP_400_BAD_REQUEST)
        client = Client.objects.get(uuid=client_uuid)
    except Client.DoesNotExist:
        return Response({'error': 'Invalid client_uuid'}, status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.get(client = client)
    project_serializer = ProjectSerializer_client(project)
    project_basic = ProjectBasic.objects.get(project = project)
    basic_project_serializer = BasicProjectSerializer(project_basic)
    serializer = ClientUpdateSerializer(client)
    context = {
        "client" : serializer.data,
        "project" : project_serializer.data,
        "basic_project" : basic_project_serializer.data,
    }
    return Response(context, status=status.HTTP_200_OK)

@api_view(['POST'])
def client_create_view(request,viewer_uuid):
    try:
        viewer = Marketing.objects.get(uuid=viewer_uuid)
    except:return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)
    client_data=request.data 
    client_serializer = ClientSerializer(data=client_data)
    client_serializer.is_valid(raise_exception=True)
    
    client = client_serializer.save()
    client.add_by = viewer
    client.save()
    project_data = {
        'name': client.name + '-' + client.location,
        'client': client.id,
        'assign_to_2d_designer': None,
        'assign_to_3d_designer': None,
        'viewer': None,
        'technical_user': None
        # Add other required fields for the Project model
    }
    print(project_data)
    project_serializer = ProjectSerializer_client(data=project_data)
    project_serializer.is_valid(raise_exception=True)
    project = project_serializer.save()
    print(project)
    basic_project_data = {
        'project': project.id,
        # Add other required fields for the BasicProject model
    }

    basic_project_serializer = BasicProjectSerializer(data=basic_project_data)
    basic_project_serializer.is_valid(raise_exception=True)
    basic_project_serializer.save()
    print(basic_project_serializer)
    print("done")
    print(client_serializer.data)
    # print( basic_project_serializer)
    context = {
        "client" : client_serializer.data,
        "project" : project_serializer.data,
        # "basic_project" : basic_project_serializer.data,
    }
    return Response(context, status=status.HTTP_201_CREATED)
# class ClientCreateView(generics.CreateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     lookup_field = 'uuid'

#     def create(self, request, *args, **kwargs):
#         client_serializer = self.get_serializer(data=request.data)
#         client_serializer.is_valid(raise_exception=True)
#         client = self.perform_create(client_serializer)

#         project_data = {
#             'name': client.name + '-' + client.location,
#             'client': client.id,
#             'assign_to_2d_designer': None,
#             'assign_to_3d_designer': None,
#             'viewer': None,
#             'technical_user': None
#             # Add other required fields for the Project model
#         }

#         project_serializer = ProjectSerializer_client(data=project_data)
#         project_serializer.is_valid(raise_exception=True)
#         project = self.perform_create(project_serializer)

#         basic_project_data = {
#             'project': project.id,
#             # Add other required fields for the BasicProject model
#         }

#         basic_project_serializer = BasicProjectSerializer(data=basic_project_data)
#         basic_project_serializer.is_valid(raise_exception=True)
#         self.perform_create(basic_project_serializer)

#         headers = self.get_success_headers(basic_project_serializer.data)
#         return Response(basic_project_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         return serializer.save()

@api_view(['GET'])
def client_retrieve_view(request,marketing_uuid):
    try:
        markting_person = Marketing.objects.get(uuid = marketing_uuid)
    except:
        return Response({'error': 'markting_person not found'}, status=400)
    try:
        client_uuid = request.data.get('client_uuid')
    except:
        return Response({'error': 'client_uuid not found'}, status=400)
    if client_uuid:
        try:
            instance = Client.objects.get(uuid=client_uuid)
            # instance.is_viewer_viewed = True
            # instance.save()
            serializer = ClientSerializer(instance)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=404)
    else:
        return Response({'error': 'client_uuid not provided in the request body'}, status=400)
@api_view(['GET'])
def get_all_clients(request, marketing_uuid):
    try:
        markting_person = Marketing.objects.get(uuid = marketing_uuid)
    except:
        return Response({'error': 'markting_person not found'}, status=400)
    clients = Client.objects.all()
    return Response(ClientSerializer(clients,many= True).data, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_all_projects(request, viewer_uuid):
    try:
        viewer = Viewer.objects.get(uuid=viewer_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Viewer not found'}, status=400)

    clients = Client.objects.filter(is_viewer_viewed=True)
    res = []
    for client in clients:
        if 33 <=  client.calculate_data_completion_percentage <= 90 :
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
        if 33 <=  client.calculate_data_completion_percentage <= 50:
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
    res_approved = []
    for client in clients:
        if client.calculate_data_completion_percentage >= 50 and client.calculate_data_completion_percentage <= 90:
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

    return Response({'clients': client_data,"needs_action":client_data_need_actions,'approved':client_data_approved})
@api_view(['GET'])
def get_all_clients_viewer(request, viewer_uuid):
    try:
        viewer = Viewer.objects.get(uuid=viewer_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Viewer not found'}, status=400)

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
        if client.calculate_data_completion_percentage <= 90:
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
    res_approved = []
    for client in clients:
        if client.calculate_data_completion_percentage >= 20 and client.calculate_data_completion_percentage <= 90:
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

    return Response({'clients': client_data,"needs_action":client_data_need_actions,'approved':client_data_approved})


@api_view(['GET'])
def get_all_clients_viewer_today_meetings(request, viewer_uuid):

    ''' getting all viewer today meetings'''
    try:
        viewer  = Viewer.objects.get(uuid = viewer_uuid)
    except:
        return Response({'error': 'viewer  not found'}, status=400)
    current_date = datetime.now().date()
    clients = Client.objects.filter(meeting_time__date=current_date )
    return Response(ClientSerializer(clients,many= True).data, status=status.HTTP_200_OK)




class ClientByUUIDView(APIView):
    def get(self, request, uuid):
        client_api = ClientAPI()
        client_data = client_api.get_client_by_uuid(uuid)
        if client_data:
            return Response(client_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        

class ClientRegistrationView(APIView):
    def post(self, request):
        serializer = ClientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            client_api = ClientAPI()
            client = client_api.register_client(
                serializer.validated_data['name'],
                serializer.validated_data['email'],
                serializer.validated_data['number']
            )
            client_data = ClientSerializer(client).data
            return Response(client_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




import asyncio
from threading import Thread
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ContactUsView(View):
    async def send_email(self, name, email):
        subject = 'Thank you for contacting us!'
        message = f"Dear {name},\n\nThank you for contacting us. We have received your message and will get back to you soon.\n\nBest regards,\nYour Organization"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

    def process_contact_form(self, name, email, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_email_task():
            await self.send_email(name, email)
        
        loop.run_until_complete(run_email_task())
        loop.close()

    def post(self, request):
        serializer = ContactSerializer(data=request.POST)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            # thread = Thread(target=self.process_contact_form, args=(name, email, message))
            # thread.start()
            # thread.join(timeout=5)

            # if thread.is_alive():
                # Thread took longer than one second, raise an error
                # return JsonResponse({'error': 'Email sending took too long.'}, status=500)
            # else:
                # Thread completed within one second, return a success response
            return JsonResponse({'message': 'Thank you for contacting us! We will get back to you soon.'})
        else:
            # Return a validation error response
            return JsonResponse(serializer.errors, status=400)
        

@api_view(['GET'])     
def client_data(request, client_uuid):
    try:
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
@api_view(['GET'])     
def client_data_pics(request, client_uuid):
    try:
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


class ClientRegistrationAPIView(APIView):
    def post(self, request):
        serializer = ClientWebSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data.get('mobile')
            email = serializer.validated_data.get('email')
            
            if not mobile and not email:
                return Response({'error': 'Mobile or email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)