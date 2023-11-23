import re
import requests
from project.models import Project
from project.serializers import ProjectSerializer, ProjectSerializer_client
from rest_framework import generics, status
from rest_framework.response import Response
from technical.models import Technical
from .models import ChatBoot, ChatState, Designer
from .serializers import ChatBootSerializer, DesignerSerializer

class DesignerListAPIView(generics.ListAPIView):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer

    def get(self, request, technical_uuid, *args, **kwargs):
        try:
            technical = Technical.objects.get(uuid=technical_uuid)
        except Technical.DoesNotExist:
            return Response({'error': 'Invalid secret key, please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)

        return super().get(request, *args, **kwargs)\
        


class AssignDesignersAPIView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer_client
    lookup_field = "uuid"
    def update(self, request, technical_uuid, *args, **kwargs):
        try:
            technical = Technical.objects.get(uuid=technical_uuid)
        except Technical.DoesNotExist:
            return Response({'error': 'Invalid secret key, please contact support construction'}, status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object()

        designer_2d_id = request.data.get('designer_2d')
        if designer_2d_id:
            try:
                designer_2d = Designer.objects.get(uuid=designer_2d_id)
            except Designer.DoesNotExist:
                return Response({'error': f"Invalid 2D designer ID: {designer_2d_id}"}, status=status.HTTP_400_BAD_REQUEST)
            project.assign_to_2d_designer = designer_2d

        designer_3d_id = request.data.get('designer_3d')
        if designer_3d_id:
            try:
                designer_3d = Designer.objects.get(uuid=designer_3d_id)
            except Designer.DoesNotExist:
                return Response({'error': f"Invalid 3D designer ID: {designer_3d_id}"}, status=status.HTTP_400_BAD_REQUEST)
            project.assign_to_3d_designer = designer_3d

        project.save()

        serializer = self.get_serializer(project)
        return Response(serializer.data)
    


# messenger/views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt
def webhook(request):
    print(1)
    
    if request.method == 'GET':
        # Verify token for webhook setup
        verify_token = request.GET.get('hub.verify_token')
        if verify_token == settings.MESSENGER_VERIFY_TOKEN:
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            return HttpResponse('Invalid verification token')
    
    
    elif request.method == 'POST'  :
        # Handle incoming messages
        data = json.loads(request.body.decode('utf-8'))
        print(data, "comming data")
        for entry in data['entry']:
            # print(entry)
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                try:
                    message_text = messaging_event['message']['text']
                except: 
                    print("error detect 500")
                    message_text =  "السلام عليكم"
                # Handle the message and craft a response
                # (we'll implement this later)
                response_text = get_response(message_text)
                # Send the response back to the user
                send_message(sender_id, response_text)
        return HttpResponse()
    

def get_response(message_text):
    # Implement your logic to generate a response here
    # print(message_text)
    if  not ChatState.objects.last().works :
        return f" "
    print(check_phone_number(f'{message_text}'))
    if check_phone_number(f'{message_text}'):
        print(4)
        return " شكرا لاضافة الرقم الخاص بك  سوف يقوم احد موظفونا بالتواصل معك  كمايمكنك المتابعة وموافاتنا بالعنوان لتحديد موعد للزياره "
    try:
        chat  = ChatBoot.objects.get(message =f'{message_text}')
    except: return  "سوف يقوم احد موظفونا بالرد عليك ف اقرب فرصة ممكن تتواصل معانا عن طريق الرقم ☎️ 01003234531"
    try:
        serialize = ChatBootSerializer(chat)
    except: return "220 هناك مشكلة بالسيرفر جاري العمل عليها"
    try:
        data  = serialize.data
    except: return " 230 هناك مشكلة بالسيرفر جاري العمل عليها"
    try:
        if data['response'] !=  None :
            return f"{data['response']}" "    "
        else:
            return 'اعتذر لعدم قدرتي علي  فهم ذلك سوف يقوم احد موظفونا بالرد ف اسرع وقت'
    except: return " 240 هناك مشكلة بالسيرفر جاري العمل عليها"
    
    
def check_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    # Check if the phone number starts with a plus sign, indicating an international number
    if phone_number.startswith('+'):
        pattern = r'^\+\d{1,3}\s?\d{11,}$'  # Pattern for international numbers
    else:
        pattern = r'^\d{11,}$' # Pattern for numbers without country code (assumes all digits)

    # Use the re.match() function to check if the phone number matches the pattern
    match = re.match(pattern, phone_number)
    print(match, "match")
    # Return True if the phone number matches the pattern, False otherwise
    return bool(match)


def send_message(recipient_id, message_text):
    params = {
        'access_token': settings.MESSENGER_PAGE_ACCESS_TOKEN
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': message_text
        }
    }
    response = requests.post(
        'https://graph.facebook.com/v14.0/me/messages',
        params=params,
        headers=headers,
        json=data
    )
    if response.status_code != 200:
        print('Failed to send message:', response.text)
