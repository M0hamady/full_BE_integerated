from django.shortcuts import get_object_or_404, redirect, render
from markting.models import Marketing
from markting.serializers import MarktingSerializer
from rest_framework.response import Response
from rest_framework import status
from client.models import Client, ClientAction
from django.core.paginator import Paginator
from django.views.generic import FormView, TemplateView

from rest_framework.decorators import api_view

from project.slck import send_slack_notification
# Create your views here.
#create check for is markting team or not

@api_view(['GET'])
def checkLicenseMarkting(request,markting_uuid):
    try:
        Markting_person = Marketing.objects.get(uuid = markting_uuid)
    except: return Response({'error': 'Invalid secret key please contact support construction'}, status=status.HTTP_400_BAD_REQUEST) 
    return Response(MarktingSerializer(Markting_person).data, status=status.HTTP_200_OK)
from django.contrib.auth.mixins import LoginRequiredMixin

def update_meeting_time(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        meeting_time = request.POST.get('meeting_time')
        client.meeting_time = meeting_time
        client.save()
    send_slack_notification("#customer-service",f"{client.name}   تم اضافة معاد جديد للمعاينة  {client.meeting_time} لترتفع نسبة اجراءات التعاقد معه واحتماليات التعاقد الي : {client.calculate_data_completion_percentage2()}" )
    return redirect('CustomerServicesView')

class UpdateNotesView(TemplateView):
    template_name = 'markting/uodate_client_notes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_action_id = self.kwargs['client_action_id']
        client_action = get_object_or_404(ClientAction, id=client_action_id)
        context['client_action'] = client_action
        return context

    def post(self, request, *args, **kwargs):
        client_action_id = self.kwargs['client_action_id']
        client_action = get_object_or_404(ClientAction, id=client_action_id)
        # Update the notes here using the posted data
        client_action.notes = request.POST.get('notes')
        client_action.save()
        return redirect('CustomerServicesView')

class CustomerServicesView(LoginRequiredMixin,TemplateView):
    template_name = "markting/customerDeals.html"
    paginate_by = 10  # Number of items to show per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the client object
        clients = Client.objects.all()
        clients_res =[client for client in clients if client.calculate_data_completion_percentage2() <=17]
        # Retrieve the client's projects

        # Create a paginator object
        paginator = Paginator(clients_res, self.paginate_by)

        page_number = self.request.GET.get('page')  # Get the current page number from the request's GET parameters
        page = paginator.get_page(page_number)  # Get the current page from the paginator

        context['page'] = page
        context['clients'] = page.object_list  # Use the steps from the current page
        return context
    
 