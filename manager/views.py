import json
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from requests import Response
from client.serializers import ClientSerializer
from fuzzywuzzy import fuzz
# Create your views here.
# all projects control 
# each project >>>>
# sea last update
# next step
# budget
# 
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import datetime, timedelta

from client.models import Client
from project.serializers import ProjectStudySerializer
from .forms import ProjectImage2DForm, ReplyCommentImage2DForm, ReplyForFeeds
from project.models import CeilingDecoration, CeilingGypsumBoard, CeramicExisted, ClientOpenToMakeEdit, CommentImage2D, DesignStyle, DoorProvided, Feedback, FlooringMaterial, Furniture, Heater, LightingType, PlumbingEstablished, Project, ProjectBasic, ProjectImage2D, ProjectStudy, ReplyCommentImage2D, SitesManager, ToiletType, WallDecorations
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
        print(user.is_viewer(), "is viewer")
        if user.is_manager() or user.is_superuser:
            return redirect('meeting')
        elif user.is_viewer():
            return redirect('viewer_dash')
        elif user.is_designer():
            return redirect('viewer_dash')
        elif user.is_branchEng():
            return redirect('site_eng')
        elif user.is_branchManager():
            return redirect('site_manager')
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
        elif query1 == 'manager':
            user = self.request.user
            branch = SitesManager.objects.get(user=user).branch
            projects = Project.objects.filter(branch=branch)
            project_ids = [project.client.id for project in projects]
            clients=Client.objects.filter(id__in=project_ids) 





        # Filter the Client objects based on the queries
        # clients = Client.objects.filter(query1=query1, query2=query2)

        context['clients'] = clients
        context['query1'] = query1
        context['query2'] = query2
        return context
  
class UpdateProjectStudyView(UpdateView):
    model = ProjectStudy
    form_class = ProjectStudyForm
    template_name = 'branches/projects/create_project_study.html'
    success_url = '/project-study/create/'
    def get_success_url(self):
        client_uuid = self.object.project.client.uuid
        return reverse('create_project_study_teamViewer', args=[client_uuid])
class Monitoring2DAnd3DImagesForProject(TemplateView):
    template_name = 'branches/projects/monitor_2d_3d_images.html'

    def get(self, request, *args, **kwargs):
        project_uuid = kwargs['project_uuid']
        self.client = Client.objects.get(uuid =project_uuid)
        self.project = get_object_or_404(Project, client=self.client.id)
        images = ProjectImage2D.objects.filter(project=self.project)
        image_comments = []
        for image in images:
            comments = CommentImage2D.objects.filter(project_image=image)
            comment_replies = []
            for comment in comments:
                replies = ReplyCommentImage2D.objects.filter(comment=comment)
                comment_replies.append(replies)
            image_comments.append((image, comments, comment_replies))
        reply_form = ReplyCommentImage2DForm()
        print(reply_form.as_ul)
        return self.render_to_response({'images': image_comments, 'client': self.client.uuid ,'reply_form': reply_form})

    def post(self, request, *args, **kwargs):
        form = ProjectImage2DForm(request.POST, request.FILES)
        project_uuid = kwargs['project_uuid']
        reply_form = ReplyCommentImage2DForm(request.POST)
        self.client = Client.objects.get(uuid =project_uuid)
        if form.is_valid():
            image = form.save(commit=False)
            image.project =  get_object_or_404(Project, client  = self.client.id)
            image.save()
            return redirect('monitor_images',self.client.uuid  )
        elif reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = CommentImage2D.objects.get(uuid=request.POST['comment_uuid'])
            reply.save()
            return redirect('monitor_images',self.client.uuid  )
        else:
            return self.render_to_response({'form': form})
        

class CreateProjectStudyView(TemplateView):
    template_name = 'branches/projects/create_project_study.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.kwargs.get('uuid')  # Get the UUID from the URL parameters
        print(uuid)
        try:
            current_project = Project.objects.get(client__uuid=uuid)  # Retrieve the current project
            project_studies = ProjectStudy.objects.filter(project=current_project)  # Retrieve current project studies
            form = ProjectStudyForm(current_project=current_project)  # Create an empty form
            existing_project_names = [project.title for project in ProjectStudy.objects.all()]
            suggestions = []

            for name in existing_project_names:
                is_similar = False

                for suggestion in suggestions:
                    similarity_ratio = fuzz.ratio(name, suggestion)

                    if similarity_ratio >= 65:
                        is_similar = True
                        break

                if not is_similar:
                    suggestions.append(name)

            suggestions = ProjectStudy.objects.filter(title__in=suggestions)# Retrieve all studies as suggestions
        except Project.DoesNotExist:
            form = ProjectStudyForm(initial={'uuid': uuid})  # Create a new form with the UUID initial value
            project_studies = []
            existing_project_names = [project.title for project in ProjectStudy.objects.all()]
            suggestions = []

            for name in existing_project_names:
                is_similar = False

                for suggestion in suggestions:
                    similarity_ratio = fuzz.ratio(name, suggestion)

                    if similarity_ratio >= 65:
                        is_similar = True
                        break

                if not is_similar:
                    suggestions.append(name)

            suggestions = ProjectStudy.objects.filter(title__in=suggestions)# Retrieve all studies as suggestions
        
        context['form'] = form
        context['client'] = Client.objects.get(uuid=uuid)
        context['uuid'] = uuid
        context['project_study'] = project_studies
        context['current_project'] = current_project
        context['suggestions'] = suggestions
        
        # Set initial value for form_reply
        feed_id = self.request.POST.get('feed_id')  # Get the feed_id from the request
        initial_reply = {'feedback': feed_id} if feed_id else {}  # Set initial value if feed_id is provided
        context['form_reply'] = ReplyForFeeds(initial=initial_reply)

        return context

    def post(self, request, *args, **kwargs):
        current_project = self.get_context_data().get('current_project')  # Retrieve the current project object
        form = ProjectStudyForm(request.POST, current_project=current_project)
        form_reply = ReplyForFeeds(request.POST)
        print(form_reply.is_valid(),form_reply.errors)
        if form.is_valid():
            form.save()
            return redirect('create_project_study_teamViewer', self.get_context_data().get('uuid'))
        elif form_reply.is_valid():
            reply = form_reply.save(commit=False)
            reply.save()
            feedback = Feedback.objects.get(id=reply.feedback.id)
            feedback.replies.add(reply.id)
            feedback.save()
            return self.render_to_response(self.get_context_data(form=form))
     
        else:
            return self.render_to_response(self.get_context_data(form=form))

def create_project_studies(request, study_uuid):
    # Check if the request method is post
    if request.method == 'POST':
        project = get_object_or_404(Project, uuid=study_uuid)
        # Get the request body as a JSON object
        data = json.loads(request.body)
        # Get the list of studies from the data
        list_studies = data.get('list_studies')
        # Check if the list is not empty
        if list_studies:
            # Loop through the list of studies
            for study in list_studies:
                # Get the title, price, count, start date, and end date from the study
                title = study.get('title')
                price = study.get('price')
                count = study.get('count')
                start_date = study.get('startDate')
                end_date = study.get('endDate')

                # Add validation for start date and end date
                start_date = datetime.today()
                
                end_date = (datetime.today() + timedelta(days=1))
                # Create a new ProjectStudy object with the given data
                new_study = ProjectStudy.objects.create(
                    project=project,
                    title=title,
                    price=float(price),
                    count=int(count),
                    start_date=start_date,
                    end_date=end_date
                )
                # Save the new study to the database
                new_study.save()
            # Return a JSON response with a success message and the list of created studies
            serializer = ProjectStudySerializer(ProjectStudy.objects.all(), many=True)
            return JsonResponse({'message': 'Project studies created successfully', 'data': serializer.data})
        else:
            # Return a JSON response with an error message
            return JsonResponse({'message': 'No studies provided'})
    else:
        # Return a JSON response with an error message
        return JsonResponse({'message': 'Invalid request method'})

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

class ProfileUpdateAPIView(APIView):
    # Define a method to handle GET requests
    def get(self, request, client_uuid):
        # Get the client object from the database or raise a 404 error if not found
        client = get_object_or_404(Client, uuid=client_uuid)
        # Serialize the client object to a JSON format
        serializer = ClientSerializer(client)
        # Return a response with the serialized data
        return Response(serializer.data)

    # Define a method to handle POST requests
    def post(self, request, client_uuid):
        # Get the client object from the database or raise a 404 error if not found
        client = get_object_or_404(Client, uuid=client_uuid)
        # Deserialize the request data to a client object
        serializer = ClientSerializer(client, data=request.data)
        # Check if the data is valid
        if serializer.is_valid():
            # Save the updated client object to the database
            serializer.save()
            # Return a response with the updated data
            return Response(serializer.data)
        else:
            # Return a response with the validation errors
            return Response(serializer.errors)
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
