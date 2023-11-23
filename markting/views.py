from django.shortcuts import render
from markting.models import Marketing
from markting.serializers import MarktingSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
#create check for is markting team or not

@api_view(['GET'])
def checkLicenseMarkting(request,markting_uuid):
    try:
        Markting_person = Marketing.objects.get(uuid = markting_uuid)
    except: return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST) 
    return Response(MarktingSerializer(Markting_person).data, status=status.HTTP_200_OK)