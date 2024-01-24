from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
# Create your views here.
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from project.models import FeedbackFloor, Floor, Project, ReplyFloor, SiteEng, SitesManager, Step, StepImage
from teamview.serializers import ViewerSerializer
from.models import Viewer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from client.models import Client
from datetime import date
from django.db.models import Q
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

def upload_photo(request, step_id):
    if request.method == 'POST':
        step = Step.objects.get(id=step_id)
        photo = request.FILES['photo']
        step_image = StepImage(step=step, image=photo)
        step_image.save()
    return redirect('site_eng_tasks',step.floor.id)    

def delete_photo(request, step_id):
    if request.method == 'POST':
        step_image_id = request.POST['step_image_id']
        StepImage.objects.filter(id=step_image_id).delete()
    return redirect('site_eng')    
def finish_step(request, step_id):
    step = get_object_or_404(Step, id=step_id)

    # Update the status of the step
    if step.status != 'finished':
        step.status = 'finished'
        step.save()
        messages.success(request, 'Step finished successfully.')
    else:
        messages.info(request, 'Step is already finished.')

    return redirect('site_eng_tasks',step.floor.id)    



def reply_feed(request, feed_id):
    feed = get_object_or_404(FeedbackFloor, id=feed_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        current_user = request.user
        # Create a new reply
        reply = ReplyFloor(
            feedback_floor=feed,
            site_Eng=SiteEng.objects.get(user=current_user),  # Set the site engineer based on the authenticated user
            message=message
        )
        reply.save()
        
        # Add the reply to the feed's replies
        feed.replies.add(reply)
        
        # Redirect back to the feed page
        return redirect('site_eng')
    
    return render('site_eng')  # Replace 'your_template.html' with the actual template name


class ProfileSiteEngTasksToday(LoginRequiredMixin, TemplateView):
    template_name = 'teamViewer/list_tasks_site_eng.html'

    def get(self, request, *args, **kwargs):
        # Access the current user
        current_user = request.user

        try:
            site_eng = SiteEng.objects.get(user=current_user)
        except SiteEng.DoesNotExist:
            raise Http404("You are not authorized as a Site Engineer.")
        
        floors = Floor.objects.filter(site_eng=site_eng)
        today = date.today()
        list_steps = []
        for floor in floors:
            steps = floor.step_set.filter(
                (Q(start_date__lte=today) | Q(end_date__lte=today) ) 
            )
            list_steps.extend(steps)
        
        context = {
            'steps': list_steps,
        }

        return render(request, self.template_name, context)
class ProfileSiteEngTasks(LoginRequiredMixin, TemplateView):
    template_name = 'teamViewer/list_tasks_site_eng.html'
    # دة البيظهر الفلورز او النقط الرايسية للانجنير 
    def get(self, request, *args, **kwargs):
        # Access the current user
        current_user = request.user

        try:
            site_eng = SiteEng.objects.get(user=current_user)
        except SiteEng.DoesNotExist:
            raise Http404("You are not authorized as a Site Engineer.")
        
        floor_id = kwargs.get('floor_id')
        
        # Retrieve the floor using the ID
        floor = get_object_or_404(Floor, id=floor_id,)

        # Retrieve the steps for the floor
        steps = floor.steps()

        context = {
            'floor': floor,
            'steps': steps,
        }

        return render(request, self.template_name, context)
class ProfileSiteEng(LoginRequiredMixin, TemplateView):
    template_name = 'teamViewer/list_tasks.html'
    # دة البيظهر الفلورز او النقط الرايسية للانجنير 
    def get(self, request, *args, **kwargs):
        # Access the current user
        current_user = request.user

        try:
            site_eng = SiteEng.objects.get(user=current_user)
        except SiteEng.DoesNotExist:
            raise Http404("You are not authorized as a Site Engineer.")
        
        floors = Floor.objects.filter(site_eng__id=site_eng.id)

        context = {
            'projects': floors,
            'test': "test re"
        }

        return render(request, self.template_name, context)
    
    
class ProfileSiteManagerProjects(LoginRequiredMixin, TemplateView):
    template_name = 'teamViewer/list_tasks.html'
# دة البيظهر الفلورز او النقط الرايسية للانجنير 
    def get(self, request, *args, **kwargs):
        # Access the current user
        current_user = request.user

        try:
            site_eng = SitesManager.objects.get(user=current_user)
        except SiteEng.DoesNotExist:
            raise Http404("You are not authorized as a Site Manager.")
        
        floors = Floor.objects.filter(site_manager__id=site_eng.id)

        context = {
            'projects': floors,
            'test': "test re"
        }

        return render(request, self.template_name, context)


class ProfileSiteManager(LoginRequiredMixin, TemplateView):
    template_name = 'teamViewer/list_tasks.html'

    def get(self, request, *args, **kwargs):
        # Access the current user
        current_user = request.user

        try:
            site_eng = SiteEng.objects.get(user=current_user)
        except SiteEng.DoesNotExist:
            raise Http404("You are not authorized as a Site Engineer.")

        projects = Project.objects.filter(floorEng__site_eng=site_eng)

        project_data = []
        for project in projects:
            floors = Floor.objects.filter(project=project)
            floors_data = []
            for floor in floors:
                steps = Step.objects.filter(floor=floor)
                floors_data.append({
                    'floor': floor,
                    'steps': steps
                })
            project_data.append({
                'project': project,
                'floors': floors_data
            })

        return render(request, self.template_name, {'projects': project_data})