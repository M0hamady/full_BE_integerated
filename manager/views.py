from django.urls import reverse
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
from project.models import CeilingDecoration, CeilingGypsumBoard, CeramicExisted, ClientOpenToMakeEdit, DesignStyle, DoorProvided, FlooringMaterial, Furniture, Heater, LightingType, PlumbingEstablished, Project, ProjectBasic, ProjectStudy, ToiletType, WallDecorations
from .forms import Profile_project_UpdateForm, ProfileUpdateForm, ProjectStudyForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, UpdateView
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
        try:
            request.user.is_viewer()
            return redirect('viewer_dash')  # Replace 'company' with the URL or name of the page you want to redirect to
        except:return super().dispatch(request, *args, **kwargs)

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
                print(today)
                clients = Client.objects.filter(meeting_time__date=today)
                print(clients,[client.meeting_time for client in Client.objects.all()])
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
                clients = [clients_d for clients_d in clients if ProjectBasic.objects.get(project__client =clients_d).project_basic_percentage() >10 ]
            elif query2 =="needs_action":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural if "markting"   in client.action_needed().split()  ]
                clients = [clients_d for clients_d in clients if ProjectBasic.objects.get(project__client =clients_d).project_basic_percentage() >30 ]

            elif query2 =="in_process":
                clients_neural = Client.objects.all()
                clients= [client for client in clients_neural if "manager"   in client.action_needed().split()  ]
                clients = [clients_d for clients_d in clients if ProjectBasic.objects.get(project__client =clients_d).project_basic_percentage() >60 ]




        # Filter the Client objects based on the queries
        # clients = Client.objects.filter(query1=query1, query2=query2)

        context['clients'] = clients
        context['query1'] = query1
        context['query2'] = query2
        return context
  
class UpdateProjectStudyView(UpdateView):
    model = ProjectStudy
    form_class = ProjectStudyForm
    template_name = 'teamViewer/create_project_study.html'
    success_url = '/project-study/create/'
    def get_success_url(self):
        client_uuid = self.object.project.client.uuid
        return reverse('create_project_study_teamViewer', args=[client_uuid])
class CreateProjectStudyView(TemplateView):
    template_name = 'teamViewer/create_project_study.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.kwargs.get('uuid')  # Get the UUID from the URL parameters
        print(uuid)
        try:
            project_study = ProjectStudy.objects.filter(project__client__uuid=uuid)
            current_project = Project.objects.get(client__uuid=uuid)  # Retrieve the ProjectStudy instances for the specified project UUID
            form = ProjectStudyForm(current_project=current_project)  # Create an empty form
        except ProjectStudy.DoesNotExist:
            form = ProjectStudyForm(initial={'uuid': uuid})  # Create a new form with the UUID initial value
        
        context['form'] = form
        context['client'] = Client.objects.get(uuid=uuid)
        context['uuid'] = uuid
        context['project_study'] = project_study
        context['current_project'] = current_project
        return context

    def post(self, request, *args, **kwargs):
        current_project = self.get_context_data().get('current_project') # Retrieve the current project object
        print(current_project.id)
        form = ProjectStudyForm(request.POST, current_project=current_project)
        print(form)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('create_project_study_teamViewer', self.get_context_data().get('uuid')  )  # Replace 'project_study_list' with the URL name for the project study list view
        else:
            return self.render_to_response(self.get_context_data(form=form))
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
            try:
                project = ProjectBasic.objects.get(uuid=client_uuid)
            except:
                return redirect('viewer_dash')
        return project

    def handle_attributes(self, request, project):
        attributes = ['location', 'dimensions', 'meters', 'hight_window', 'is_add_fur_2d', 'is_boiler', 'count_boiler', 'count_rooms', 'count_kids', 'count_kids_male', 'count_kids_female']
        for attribute in attributes:
            value = request.POST.get(attribute)
            print(attribute,value)
            if attribute == 'is_add_fur_2d' and value is None or attribute == 'is_boiler' and value is None:
                value =False
            if value is not None:
                if attribute == 'is_add_fur_2d' or attribute == 'is_boiler':
                    print(value,4747,attribute)
                    # value = value.lower() == 'true'
                    setattr(project, attribute, value)
                setattr(project, attribute, str(value))

    def handle_foreign_keys(self, request, project):
        foreign_key_fields = {
            'clientOpenToMakeEdit': ClientOpenToMakeEdit,
            'plumbingEstablished': PlumbingEstablished,
            'ceilingGypsumBoard': CeilingGypsumBoard,
            'doorProvided': DoorProvided,
            'ceramicExisted': CeramicExisted,
            'toiletType': ToiletType,
            'heater': Heater
        }
        for attribute, model_class in foreign_key_fields.items():
            value = request.POST.get(attribute)
            if value is not None and value != "":
                try:
                    instance = get_object_or_404(model_class, id=int(value))
                    setattr(project, attribute, instance)
                except ValueError:
                    # Handle the case when the value cannot be converted to an integer
                    # You can choose to ignore it, raise an error, or handle it differently
                    pass

    def get(self, request, client_uuid):
        project = self.get_project(client_uuid)
        form = Profile_project_UpdateForm(instance=project)
        return render(request, self.template_name, {'form': form, 'project': project})

    def post(self, request, client_uuid):
        project = self.get_project(client_uuid)
        self.handle_attributes(request, project)
        self.handle_foreign_keys(request, project)
        project.save()
        print(request.POST)

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
    
def add_style(request, project_uuid, style_uuid):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    # style = request.POST.get("style__add")
    print(style_uuid)
    design_style= get_object_or_404(DesignStyle, name=style_uuid)
    project.design_styles.add(design_style)
    project.save()
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,"url_name_delete":"/client/design/delete/",'tag':'tag1','list_options':project.design_styles.all(),})
def delete_design(request, project_uuid, style_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    color = request.POST.get("design")
    # design_color, created = DesignColors.objects.get_or_create(name=color)
    # print(design_color.id)
    project.design_styles.remove(style_id)
    project.save()
    success_message = 'Color successfully deleted.'
    print(success_message,color)
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,'list_options':project.design_styles.all(),"url_name_delete":"/client/design/delete/",'tag':'tag1', 'success_message': success_message})

# re[eat]
def add_ceiling_decorations(request, project_uuid, style_uuid):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    # style = request.POST.get("style__add")
    design_style= get_object_or_404(CeilingDecoration, name=str(style_uuid).replace("_"," "))
    print(style_uuid,project)
    project.ceiling_decoration.add(design_style)
    project.save()
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,"url_name_delete":"/client/ceiling/delete/",'tag':'tag2','list_options':project.ceiling_decoration.all(),})
def delete_ceiling_decorations(request, project_uuid, style_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    project.ceiling_decoration.remove( style_id)
    project.save()
    success_message = 'ceiling deleted.'
    print(success_message)
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,'list_options':project.ceiling_decoration.all(),"url_name_delete":"/client/ceiling/delete/",'tag':'tag2', 'success_message': success_message})
# end repeat
# re[eat]
def add_light_type(request, project_uuid, light_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    # style = request.POST.get("style__add")
    light_type= get_object_or_404(LightingType, name=str(light_id).replace("_"," "))
    print(light_type,project)
    project.lighting_type.add(light_type.id)
    project.save()
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,"url_name_delete":"/client/light_type/delete/",'tag':'tag3','list_options':project.lighting_type.all(),})
def delete_light_type(request, project_uuid, light_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    project.lighting_type.remove( light_id)
    project.save()
    success_message = 'lighting_type successfully deleted.'
    print(success_message)
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,'list_options':project.lighting_type.all(),"url_name_delete":"/client/lighting_type/delete/",'tag':'tag3', 'success_message': success_message})
# end repeat
# re[eat]
def add_wall_decorations(request, project_uuid, wall_id):
    print(wall_id)
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    # style = request.POST.get("style__add")
    wall_decorations= get_object_or_404(WallDecorations, name=str(wall_id).replace("_"," "))
    print(wall_decorations,project)
    project.wall_decorations.add(wall_decorations.id)
    project.save()
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,"url_name_delete":"/client/wall_decoration/delete/",'tag':'tag4','list_options':project.wall_decorations.all(),})
def delete_wall_decorations(request, project_uuid, wall_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    project.wall_decorations.remove( wall_id)
    project.save()
    success_message = 'wall_decoration deleted.'
    print(success_message)
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,'list_options':project.wall_decorations.all(),"url_name_delete":"/client/wall_decoration/delete/",'tag':'tag4', 'success_message': success_message})
# end repeat
# re[eat]
def add_flooring_material(request, project_uuid, flooring_id):
    print(flooring_id,"floor",project_uuid)
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    # style = request.POST.get("style__add")
    flooring_material= get_object_or_404(FlooringMaterial, name=str(flooring_id).replace("_"," "))
    print(flooring_material,project)
    project.flooring_material.add(flooring_material.id)
    project.save()
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,"url_name_delete":"/client/flooring/delete/",'tag':'tag5','list_options':project.flooring_material.all(),})
def delete_flooring_material(request, project_uuid, flooring_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    project.flooring_material.remove( flooring_id)
    project.save()
    success_message = 'flooring successfully deleted.'
    print(success_message)
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,'list_options':project.flooring_material.all(),"url_name_delete":"/client/flooring/delete/",'tag':'tag5', 'success_message': success_message})
# end repeat
# re[eat]
def add_furniture_details(request, project_uuid, furniture_id):
    print(furniture_id,"floor",project_uuid)
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    # style = request.POST.get("style__add")
    furniture= get_object_or_404(Furniture, name=str(furniture_id).replace("_"," "))
    print(furniture,project)
    project.furniture.add(furniture.id)
    project.save()
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,"url_name_delete":"/client/furniture/delete/",'tag':'tag6','list_options':project.furniture.all(),})
def delete_furniture_details(request, project_uuid, furniture_id):
    project = get_object_or_404(ProjectBasic, uuid=project_uuid)
    project.furniture.remove( furniture_id)
    project.save()
    success_message = 'furniture successfully deleted.'
    print(success_message)
    return render(request, 'teamViewer/widjet/list_obtions.html', {'project': project,'list_options':project.furniture.all(),"url_name_delete":"/client/furniture/delete/",'tag':'tag6', 'success_message': success_message})
# end repeat

def design_styles(request,):
    design_styles = DesignStyle.objects.all()
    context = {'design_styles': design_styles}
    return render(request, 'teamViewer/team_partials/designe_Decoration_Ceiling/list_designe.html', context)
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
