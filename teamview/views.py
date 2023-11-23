from django.shortcuts import render

# Create your views here.
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from teamview.serializers import ViewerSerializer
from.models import Viewer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from client.models import Client

@api_view(['GET'])
def check_viewer_uuid(request, uuid):
    try:
        viewer = Viewer.objects.get(uuid=uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Viewer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ViewerSerializer(viewer)
    return Response(serializer.data)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'teamViewer/nudex.html'

    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        
        return render(request, self.template_name, {'clients': clients})