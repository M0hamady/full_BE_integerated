from django.shortcuts import render, get_object_or_404

# Create your views here.
# all projects control 
# each project >>>>
# sea last update
# next step
# budget
# 
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import timedelta

from client.models import Client
from project.models import DesignStyle, Project, ProjectBasic
from .forms import Profile_project_UpdateForm, ProfileUpdateForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect

class Login(LoginView):
    template_name = 'registration/login.html'
    def form_valid(self, form):
        # Log in the user
        user = form.get_user()
        login(self.request, user)
        print(user.is_manager(),user.is_viewer())
        print(user.is_viewer(), "is viewer")
        if user.is_manager():
            return redirect('meeting')
        elif user.is_viewer():
            return redirect('viewer_dash')
        # return redirect('meeting')
        
       

        return super().form_valid(form)
class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'manager/index.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_viewer():
            return redirect('viewer_dash')  # Replace 'company' with the URL or name of the page you want to redirect to
        return super().dispatch(request, *args, **kwargs)

class Projects(LoginRequiredMixin, TemplateView):
    template_name = 'registration/pages/projects.html'

class Meeting(LoginRequiredMixin, TemplateView):
    template_name = 'registration/pages/meetings.html'
class ClientFilterView(TemplateView):
    template_name = 'teamViewer/list_clients.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query1 = kwargs.get('query1')
        query2 = kwargs.get('query2')
        if query1 == 'from_markting':
            if query2 == "clients":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural ]
            elif query2 =="needs_actions":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural if client.calculate_data_completion_percentage >= 30 ]
                
            elif query2 =="in_process":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural if client.calculate_data_completion_percentage <= 30 and client.calculate_data_completion_percentage >= 50]
                
        elif query1 == "meetings":
            if query2 =="today":
                today = timezone.now().date()
                clients = Client.objects.filter(meeting_time=today)
                
            elif query2 =="this_week":
                today = timezone.now().date()
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                clients = Client.objects.filter(meeting_time__date__range=[start_of_week, end_of_week])
            elif query2 =="upcoming":
                today = timezone.now().date()
                clients = Client.objects.filter(meeting_time__date__gt=today)
        elif query1 == "tech_team":
            if query2 =="clients":
                clients = Client.objects.all()
            elif query2 =="needs_action":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural if "markting"   in client.action_needed().split()  ]
            elif query2 =="in_process":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural if "manager"   in client.action_needed().split()  ]
                
        

        # Filter the Client objects based on the queries
        # clients = Client.objects.filter(query1=query1, query2=query2)

        context['clients'] = clients
        context['query1'] = query1
        context['query2'] = query2
        return context
    

def profile_update_view(request, client_uuid):
    client = get_object_or_404(Client, uuid=client_uuid)
    print("request.user.is_viewer()", request.user.is_viewer())
    if request.user.is_viewer():
        client.is_viewer_viewed =True
        client.is_active =True
        client.save()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            # Redirect to a success page or perform other actions
    else:
        form = ProfileUpdateForm(instance=client)

    return render(request, 'teamViewer/client_update.html', {'form': form, "client": client})
from django.shortcuts import render, redirect
from django.views import View
from project.models import DesignColors
from .forms import Profile_project_UpdateForm

class ProfileProjectUpdateView(LoginRequiredMixin, View):
    template_name = 'teamViewer/clientt_project.html'

    def get_project(self, client_uuid):
        try:
            client = Client.objects.get(uuid=client_uuid)
            project = ProjectBasic.objects.get(project__uuid=Project.objects.get(client=client).uuid)
        except (Client.DoesNotExist, Project.DoesNotExist, ProjectBasic.DoesNotExist):
            project = ProjectBasic.objects.get( uuid=client_uuid)
        return project

    def get(self, request, client_uuid):
        project = self.get_project(client_uuid)
        form = Profile_project_UpdateForm(instance=project)
        return render(request, self.template_name, {'form': form, 'project': project})

    def post(self, request, client_uuid):
        color= request.POST.get('color')
        project = self.get_project(client_uuid)
        color= DesignColors.objects.get_or_create(name=color)
        project.dimensions = request.POST.get('dimensions')
        project.meters = request.POST.get('meters')
        project.hight_window = request.POST.get('hight_window')
        # project.is_add_fur_2d = request.POST.get('is_add_fur_2d')
        # project.is_boiler = request.POST.get('is_boiler')
        project.count_boiler = request.POST.get('count_boiler')
        # project.count_rooms = request.POST.get('count_rooms')
        project.count_kids = request.POST.get('count_kids')
        project.count_kids_male = request.POST.get('count_kids_male')
        project.count_kids_female = request.POST.get('count_kids_female')
        project.save()
        form = Profile_project_UpdateForm(instance=project)
        
        return render(request, self.template_name, {'form': form, 'project': project})
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)



# //////////////////
def add_color(request,project_uuid):
    project = ProjectBasic.objects.get(uuid=project_uuid)
    color = request.POST.get("color__add")
    print(color)
    design_color,created = DesignColors.objects.get_or_create(name=color)
    print(design_color)
    project.design_colors.add(design_color)
    project.save()
    print('success')
    return render(request, 'teamViewer/team_partials/colors/list_colors.html', {'project': project})
    
def add_style(request, project_uuid=None, style_uuid=None):
    project = get_object_or_404(DesignStyle, uuid=project_uuid)
    # style = request.POST.get("style__add")
    print(style_uuid)
    design_style, created = get_object_or_404(DesignStyle, name=style_uuid)
    print(design_style)
    project.design_styles.add(design_style)
    project.save()
    print('success')
    return render(request, 'teamViewer/team_partials/colors/list_colors.html', {'project': project})


def design_styles(request,):
    design_styles = DesignStyle.objects.all()
    context = {'design_styles': design_styles}
    return render(request, 'teamViewer/team_partials/designe_style/list_designe.html', context)
def delete_color(request, project_uuid,color_uuid):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    color = request.POST.get("color_delete")
    # design_color, created = DesignColors.objects.get_or_create(name=color)
    # print(design_color.id)
    project.design_colors.remove(color_uuid)
    project.save()
    success_message = 'Color successfully deleted.'
    print(success_message)
    return render(request, 'teamViewer/team_partials/colors/list_colors.html', {'project': project, 'success_message': success_message})


def delete_design(request, project_uuid):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    color = request.POST.get("design")
    # design_color, created = DesignColors.objects.get_or_create(name=color)
    # print(design_color.id)
    project.design_styles.remove(color)
    project.save()
    success_message = 'Color successfully deleted.'
    print(success_message,color)
    return render(request, 'teamViewer/team_partials/list_colors.html', {'project': project, 'success_message': success_message})