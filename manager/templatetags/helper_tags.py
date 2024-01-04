from django import template
import re
from django.urls import reverse
from django.apps import apps
import mimetypes
from project.models import Project, ProjectBasic, ProjectFile
register = template.Library()

@register.filter
def to_str(value):
    # print(value,555555555)
    try:
        match = re.search(r'<option.*?>(.*?)</option>', str(value))
        if match:
            test_str = match.group(1).replace(" ", "_")
            return test_str
    except (AttributeError, IndexError, TypeError):
        pass
    return ''
@register.simple_tag
def model_links(request):
    # {name: "", list: [{name:"",link:""}]}
    model_names = []
    for model in apps.get_models():
        if model._meta.app_label =="project":
            if request.user.is_viewer() or  request.user.is_manager() or request.user.is_superuser:
                model_attrs = [attr for attr in dir(model) if not attr.startswith('_')]
                for attr in model_attrs:
                    attr_value = getattr(model, attr)
                    if model._meta.model_name in ["walldecorations","designstyle","ceilingdecoration","lightingtype","designcolors","flooringmaterial","furniture","clientopentomakeedit","plumbingestablished","ceilinggypsumboard","doorprovided","ceramicexisted","toilettype","heater","floor"] and model._meta.model_name not in [modals['name'] for modals in model_names]:
                        # print(type(model._meta.model_name),model._meta.model_name)
                        model_names.append({'name':model._meta.model_name,'link':f"/admin/project/{model._meta.model_name}/"})

    links = []
    for modal in model_names:
        
        links.append({
            'name': modal['name'],
            'link': modal['link'],
            
        })
    return links
@register.simple_tag
def project_files(uuid):
    # Get the ProjectBasic object with the given UUID
    project_basic = ProjectBasic.objects.get(uuid=uuid)

    # Get the project ID of the ProjectBasic object
    project_uuid = project_basic.project.uuid

    # Filter ProjectFile objects based on the project ID
    project_files = ProjectFile.objects.filter(project__uuid=project_uuid)

    # Filter ProjectFile objects based on the UUID

    return project_files

@register.simple_tag
def get_extensions(name):
    file_mime = mimetypes.guess_type(name)
    file_type = file_mime[0]
    print("file_type",file_type)
    if file_type:
        if file_type == 'application/pdf':
            return 'PDF'
        elif file_type == 'application/html' or 'application/x-java-jnlp-file' or 'text/html' or file_type.startswith('application/'):
            return 'CODE'
        else:
            return file_type.split('/')[0].upper()
    else:
        return None
@register.simple_tag
def get_last_file_name(file_path):
    path_arr = file_path.split('/')  # Split the file path by "/"
    file_name = path_arr[-1]  # Get the last element

    if len(file_name) > 10:
        dots_count = len(file_name) - 10
        dots = '.' * dots_count
        return file_name[:dots_count] + dots

    return file_name

@register.simple_tag
def projects_manager():
    projects = Project.objects.all()
    print([project.roadmap for project in projects])
    finished_projects = projects.filter(is_finished=True)
    current_projects = projects.filter(is_finished=False)
    print([project.is_finished for project in current_projects])
    going_to_finish = []
    going_to_start = [project for project in projects if project.client.calculate_data_completion_percentage2() < 70 and ProjectBasic.objects.get(project=project).project_basic_percentage() < 60 ]
    for project in projects:
        project_basic = ProjectBasic.objects.filter(project=project).first()
        if project_basic and project_basic.project_basic_percentage() < 30:
            going_to_start.append(project)
        if project_basic and project_basic.project_basic_percentage() > 60:
            going_to_finish.append(project)
    return {
        'projects': projects,
        'finished_projects': finished_projects,
        'current_projects': current_projects,
        'going_to_finish': going_to_finish,
        'going_to_start': going_to_start
    }