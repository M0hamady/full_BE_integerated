import logging
from django.http import HttpResponse, HttpResponseBadRequest
from project.models import *
from project.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

class AllDataAPIView(APIView):
    def get(self, request):
        wall_decorations = WallDecorations.objects.all()
        design_styles = DesignStyle.objects.all()
        ceiling_decorations = CeilingDecoration.objects.all()
        lighting_types = LightingType.objects.all()
        design_colors = DesignColors.objects.all()
        flooring_materials = FlooringMaterial.objects.all()
        furniture = Furniture.objects.all()
        high_windows = HightWindow.objects.all()

        wall_decorations_serializer = WallDecorationSerializer(wall_decorations, many=True)
        design_styles_serializer = DesignStyleSerializer(design_styles, many=True)
        ceiling_decorations_serializer = CeilingDecorationSerializer(ceiling_decorations, many=True)
        lighting_types_serializer = LightingTypeSerializer(lighting_types, many=True)
        design_colors_serializer = DesignColorsSerializer(design_colors, many=True)
        flooring_materials_serializer = FlooringMaterialSerializer(flooring_materials, many=True)
        furniture_serializer = FurnitureSerializer(furniture, many=True)
        high_windows_serializer = HighWindowSerializer(high_windows, many=True)
        one_coicers = [
        #    { 
        #         'question':'what is windows height?',
        #         'Key_updates':'hight_window',
        #        'Answers': high_windows_serializer.data},
           { 
                'question':'Client open to make edit',
                'Key_updates':'clientOpenToMakeEdit',
               'Answers': ClientOpenToMakeEditSerializer(ClientOpenToMakeEdit.objects.all(),many=True).data},
           { 
                'question':'Plumbing established?',
                'Key_updates':'Plumbing_established',
               'Answers': PlumbingEstablishedSerializer(PlumbingEstablished.objects.all(),many=True).data},
           { 
                'question':'Ceiling gypsum board ?',
                'Key_updates':'Ceiling_gypsum_board',
               'Answers': CeilingGypsumBoardSerializer(CeilingGypsumBoard.objects.all(),many=True).data},
           { 
                'question':'Door provided ?',
                'Key_updates':'Door_provided',
               'Answers': DoorProvidedSerializer(DoorProvided.objects.all(),many=True).data},
           { 
                'question':'Ceramic existed  ?',
                'Key_updates':'Ceramic_existed',
               'Answers': CeramicExistedSerializer(CeramicExisted.objects.all(),many=True).data},
           { 
                'question':'Toilet type  ?',
                'Key_updates':'toilet_type',
               'Answers': ToiletTypeSerializer(ToiletType.objects.all(),many=True).data},
           { 
                'question':'Heater?',
                'Key_updates':'heater',
               'Answers': HeaterSerializer(Heater.objects.all(),many=True).data},
        ]
        multi_chices  = [
            # {   
            #     'question':'what is the flooring material?',
            #     'Key_updates':'flooring_material',
            #     'Answers': flooring_materials_serializer.data},
            # {
            #     'question':'what do you have from?',
            #     'Key_updates':'furniture',
            #     'Answers': furniture_serializer.data},
            {
                'question':'what is the wall decoration?',
                'Key_updates':'wall_decorations',
                'Answers': wall_decorations_serializer.data},
            {
                'question':'Interior style?',
                'Key_updates':'design_styles',
                'Answers': design_styles_serializer.data},
            # {
            #     'question':'what is the ceiling decorations?',
            #     'Key_updates':'ceiling_decoration',
            #     'Answers': ceiling_decorations_serializer.data},
            {
                'question':'what is the lighting type?',
                'Key_updates':'lighting_type',
                'Answers': lighting_types_serializer.data},
            # {
            #     'question':'which colors do you prefers?',
            #     'Key_updates':'design_colors',
            #     'Answers': design_colors_serializer.data},
        ]
        add_text = [
                {
                'question':'what is windows height?',
                'Key_updates':'hight_window',
                },
                
        ]
        data = {
           "one_choices":one_coicers,
           "multi_choices":multi_chices,
           "add_text":multi_chices,
            "example_Re":'" multi option body >>>   design_colors":["79456861-5ef5-44b6-bd69-43d0ce673c21  one option body >>>   "hight_window":"4cb6973c-b04f-4e9e-b9b0-003943691bc7",'
            
        }

        return Response(data)

class ProjectBasicCreateAPIView(APIView):
    def post(self, request):
        serializer = ProjectBasicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view

@api_view(['GET'])
def project_basic_retrieve(request, viewer_uuid):
    client_uuid = request.data.get('client_uuid')
    print(request.data)
    viewer = get_object_or_404(Viewer, uuid=viewer_uuid)
    print(viewer,client_uuid)
    if not client_uuid:
        return Response({'error': 'client_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        print("155555555")
        client = get_object_or_404(Client, uuid=client_uuid)
        project = get_object_or_404(Project, client__uuid=client.uuid)
        project_basic = get_object_or_404(ProjectBasic, project__uuid=project.uuid)
        print(project_basic)
        basic_data_serializer = BasicProjectSerializer(project_basic)
        return Response(basic_data_serializer.data)
    except:
        return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['PUT'])
def update_can_sea(request, uuid):
    try:
        viewer = Viewer.objects.get(uuid=uuid)
    except Viewer.DoesNotExist:
        return Response({'error': "Unauthorized, please contact Code Ocean"}, status=status.HTTP_401_UNAUTHORIZED)

    uuid_image = request.data.get('image_uuid')
    can_client_sea = request.data.get('can_client_sea')

    try:
        image = ProjectImage.objects.get(uuid=uuid_image)
    except ProjectImage.DoesNotExist:
        return Response({'error': "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ImageSerializer(image, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.validated_data['can_client_sea'] = can_client_sea
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def update_client_approved(request, uuid):
    try:
        client = Client.objects.get(uuid=uuid)
    except Client.DoesNotExist:
        return Response({'error': "Unauthorized, please contact Code Ocean"}, status=status.HTTP_401_UNAUTHORIZED)

    study_approve = request.data.get('is_client_approved_study')
    d2_approve = request.data.get('is_client_approved_2d')
    d3_approve = request.data.get('is_client_approved_3d    ')

    project = get_object_or_404(Project , client = client )
    if study_approve :
        print(1)
        project.is_client_approved_study = True 
    if d2_approve :
        project.is_client_approved_2d = True 
    if d3_approve :
        project.is_client_approved_3d = True 
    print(project.is_client_approved_study)
    project.save()
    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['PUT'])
def update_can_sea_file(request, uuid):
    try:
        viewer = Viewer.objects.get(uuid=uuid)
    except Viewer.DoesNotExist:
        return Response({'error': "Unauthorized, please contact Code Ocean"}, status=status.HTTP_401_UNAUTHORIZED)

    uuid_file = request.data.get('uuid_file')
    can_client_sea = request.data.get('can_client_sea')

    try:
        file = ProjectFile.objects.get(uuid=uuid_file)
    except ProjectFile.DoesNotExist:
        return Response({'error': "file not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FileSerializer(file, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.validated_data['can_client_sea'] = can_client_sea
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import ProjectBasicSerializer
from rest_framework import generics
class CommentImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment_image.objects.all()
    serializer_class = CommentImageSerializer
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # Perform any additional actions before deleting the comment
        instance.delete()


def get_comments_by_image_and_client(request):
    image_uuid = request.GET.get('image_uuid')
    client_uuid = request.GET.get('client_uuid')

    if not image_uuid or not client_uuid:
        return JsonResponse({'error': 'Both image_uuid and client_uuid are required.'}, status=400)

    comments = Comment_image.objects.filter(image__uuid=image_uuid, client__uuid=client_uuid)

    data = []
    for comment in comments:
        if not comment.is_reply_1:
            comment_data = {
                'image_uuid': comment.image.uuid,
                'uuid': comment.uuid,
                'owner': comment.owner.uuid,
                'content': comment.content,
                'is_reply': comment.is_reply_1,
                'replies': [],
                'created_at': comment.created_at
            }
            data.append(comment_data)
        else:
            parent = comment.parent_uuid()
            for image in data:
                if image['uuid'] == parent:
                    image['replies'].append({
                'image_uuid': comment.image.uuid,
                'owner': comment.owner.uuid,
                'content': comment.content,
                'created_at': comment.created_at
            })

    return JsonResponse({'comments': data}, status=200)
class CommentImageAPIView(generics.ListCreateAPIView):
    serializer_class = CommentImageSerializer

    def get_queryset(self):
        queryset = Comment_image.objects.all()
        image_uuid = self.request.query_params.get('image_uuid')
        client_uuid = self.request.query_params.get('client_uuid')

        if image_uuid and client_uuid:
            queryset = queryset.filter(image__uuid=image_uuid, client__uuid=client_uuid)
        elif image_uuid:
            queryset = queryset.filter(image__uuid=image_uuid)
        elif client_uuid:
            queryset = queryset.filter(client__uuid=client_uuid)

        return queryset

    def create(self, request, *args, **kwargs):
        parent_uuid = request.data.get('parent')
        if parent_uuid:
            # Creating a reply
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            parent_comment = Comment_image.objects.get(uuid=parent_uuid)
            serializer.save(parent=parent_comment)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # Creating a comment
            request.data['uuid'] = str(request.data['image'])  # Convert the image to the appropriate data type
            return super().create(request, *args, **kwargs)
        

@api_view(['POST'])
def create_comment_options(request,uuid):
    project_basic_uuid = request.data.get('project_uuid')
    print(project_basic_uuid,4444444444)
    if  len(project_basic_uuid) <=0: 
        return Response({'error': 'project_uuid is required'}, status=404)
    try:
        project = Project.objects.get(uuid=project_basic_uuid)
        project_basic = ProjectBasic.objects.get(project= project)

    except :
        try:
            project = Project.objects.get(client__uuid=project_basic_uuid)
            project_basic = ProjectBasic.objects.get(project= project)
        except:
            return Response({'error': 'project_uuid is not correct'}, status=404)
    Key_option = request.data.get('Key_option')
    if  not Key_option: 
        return Response({'error': 'Key_option is required'}, status=404)
    print(Key_option)
    data = {
        'project_basic':project_basic.id,
        'Key_option': Key_option,
        'comment': request.data.get('comment'),
        'parent': request.data.get('parent'),
        'created_by': str(uuid),
    }
    serializer = CommentOptionsSerializer(data = data)
    if serializer.is_valid():
        comment = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def feedback_exact_floor_view(request, floor_uuid):
    if request.method == 'GET':
        # Add additional validation here
        try:
            feedback_floors = FeedbackFloor.objects.filter(floor__uuid=floor_uuid)
            serializer = FeedbackFloorSerializer(feedback_floors, many=True)
            return Response(serializer.data, status=201)
        except FeedbackFloor.DoesNotExist:
            return Response({'error': 'Floor not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def client_dash_home_data(request, client_uuid):
    if request.method == 'GET':
        # Add additional validation here
        try:
            client = Client.objects.get(uuid=client_uuid)
            project=Project.objects.get(client=client)
            client_floors = Floor.objects.filter(project = project)
            total_budget = 0
            actions = 0
            for floor in client_floors:
                total_budget += floor.calculate_budget()
                actions += floor.steps_count() 
            total_amount_payments = Payment.objects.filter(client=project.client).aggregate(total_amount=Sum('amount'))
            total_amount_payments = total_amount_payments['total_amount'] or 0
            remaining_budget = project.ref_budget - total_amount_payments
            context = {
                "budget":total_budget,
                "ref_budget":project.ref_budget,
                "actions":actions,
                "payments":total_amount_payments,
                "needed":remaining_budget,
            }
            return Response(context, status=201)
        except FeedbackFloor.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def get_project_image_by_uuid(request, client_uuid):
    try:
        project = get_object_or_404(Project,client__uuid=client_uuid)
        project_image = ProjectImage2D.objects.filter(project=project)
        serializer = ProjectImage2DSerializer(project_image, many= True)
        return Response(serializer.data, status=200)
        
    except ProjectImage2D.DoesNotExist:
        return Response({"message": "Project image not found"}, status=404)

@api_view(['POST'])
def create_project_image_by_uuid(request, client_uuid):
    try:
        client = Client.objects.get(uuid=client_uuid)
    except Project.DoesNotExist:
        return Response({"message": "client not found"}, status=404)
    project = Project.objects.get(client=client)
    data = request.data.copy()     # if i want to handle it later
    # Perform any data manipulation or validation here
    # For example, you can add additional fields or modify existing ones
    data['project'] = project.id
    serializer = ProjectImage2DSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(project=project)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(['GET'])
def get_project_image_with_comments(request, project_image_uuid,client_uuid):
    try:
        project_image = ProjectImage2D.objects.get(uuid=project_image_uuid)
        serializer = ProjectImage2DSerializer(project_image)
        comments = CommentImage2D.objects.filter(project_image=project_image).order_by('-created_at')
        comment_serializer = CommentImage2DSerializer(comments,many=True)
        response={
            'image':serializer.data,
            'comments':comment_serializer.data
        }
        return Response(response, status=200)
    except ProjectImage2D.DoesNotExist:
        return Response({"message": "Project image not found"}, status=404)

@api_view(['POST'])
def create_comment_project_image_2d(request, project_image_uuid,client_uuid):
    try:
        project_image = ProjectImage2D.objects.get(uuid=project_image_uuid)
    except ProjectImage2D.DoesNotExist:
        return Response({"message": "Project image not found"}, status=404)
    data = request.data.copy() 
    data['project_image'] = project_image.id
    serializer = CommentImage2DSerializer(data=data)
    if serializer.is_valid():
        serializer.save(project_image=project_image)
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def feedback_floor_view(request):
    if request.method == 'GET':
        feedback_floors = FeedbackFloor.objects.all()
        serializer = FeedbackFloorSerializer(feedback_floors, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FeedbackFloorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def create_comment(request):
    creator_uuid = request.data.get('uuid_creator')

    if not creator_uuid:
        return Response({'error': 'uuid_creator is required'}, status=status.HTTP_400_BAD_REQUEST)

    image_uuid = request.data.get('image_uuid')
    image = get_object_or_404(ProjectImage, uuid=image_uuid)

    try:
        client = Client.objects.get(uuid=creator_uuid)
    except Client.DoesNotExist:
        try:
            designer = Designer.objects.get(uuid=creator_uuid)
        except Designer.DoesNotExist:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment = Comment_image.objects.create(
            image=image,
            content=request.data.get('content'),
            client=client if 'client' in locals() else None,
            designer=designer if 'designer' in locals() else None
        )

        serializer = CommentImageSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProjectBasic, DesignStyle, DesignColors, CeilingDecoration, LightingType, WallDecorations, \
    FlooringMaterial, Furniture, HightWindow
class DesignColorsCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = DesignColorsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        existing_color = DesignColors.objects.filter(name=name).first()

        if existing_color:
            existing_color_serializer = DesignColorsSerializer(existing_color)
            return Response(existing_color_serializer.data, status=status.HTTP_200_OK)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import re
@api_view(['POST'])
def create_notes(request, ):
    try:
        project_basic = request.data.get('project_basic')
        try:
            project_basic = ProjectBasic.objects.get(uuid=project_basic)
        except ProjectBasic.DoesNotExist:
            return Response({'error': 'ProjectBasic not found'}, status=404)
    except:
        return Response({'error': 'project_uuid is required'}, status=404)

    serializer = NotesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(project_basic=project_basic)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)
def validate_google_maps_link(value):
    # Validate the URL format
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError("Invalid Google Maps link")

    # Validate that the URL is a Google Maps link
    if not re.match(r'^https?://(www\.)?(google\.com/maps|maps\.app\.goo\.gl)', value):
        print(1)
        raise ValidationError("Invalid Google Maps link")
@api_view(['PUT'])
def update_basic_project(request, viewer_uuid):
    viewer = get_object_or_404(Viewer, uuid=viewer_uuid)
    
    client_uuid = request.data.get('client_uuid')
    client = get_object_or_404(Client, uuid=client_uuid)
    
    project_main = get_object_or_404(Project, client=client, is_finished=False)
    project_basic = get_object_or_404(ProjectBasic, project=project_main)
    # one option choice
    clientOpenToMakeEdit = request.data.get('clientOpenToMakeEdit')
    Plumbing_established = request.data.get('Plumbing_established')
    Ceiling_gypsum_board = request.data.get('Ceiling_gypsum_board')
    Door_provided = request.data.get('Door_provided')
    Ceramic_existed = request.data.get('Ceramic_existed')
    toilet_type = request.data.get('toilet_type')
    heater = request.data.get('heater')
    # end one option choice
    # start multi choices
    design_style_uuids = request.data.get('design_styles', [])
    design_styles_comment = request.data.get('design_styles_comment')
    design_color_uuids = request.data.get('design_colors', [])
    # ceiling_decoration_uuid = request.data.get('design_colors_comment')
    lighting_type_uuid = request.data.get('lighting_type',[])
    lighting_type_comment = request.data.get('lighting_type_comment')
    ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    ceiling_decoration_comment = request.data.get('ceiling_decoration_comment')
    wall_decoration_uuids = request.data.get('wall_decorations', [])
    wall_decorations_comment = request.data.get('wall_decorations_comment')
    flooring_material_uuid = request.data.get('flooring_material')
    flooring_material_comment = request.data.get('flooring_material_comment')
    furniture_uuids = request.data.get('furniture', [])
    furniture_comment = request.data.get('furniture_comment')
    hight_window = request.data.get('hight_window')
    hight_window_comment = request.data.get('hight_window_comment')
    
    location = request.data.get('location')
    # ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    dimensions = request.data.get('dimensions')
    # ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    meters = request.data.get('meters')
    # ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    is_add_fur_2d = request.data.get('is_add_fur_2d', False)
    # ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    is_boiler = request.data.get('is_boiler', False)
    # ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    count_boiler = request.data.get('count_boiler', 0)
    # ceiling_decoration_uuid = request.data.get('ceiling_decoration')
    
    try:
        if design_style_uuids:
            design_styles = DesignStyle.objects.filter(uuid__in=design_style_uuids)
            project_basic.design_styles.set(design_styles)
            
        if design_color_uuids:
            design_colors = DesignColors.objects.filter(uuid=design_color_uuids)
            for color in design_colors:
                project_basic.design_colors.add(color)
            
        if ceiling_decoration_uuid:
            ceiling_decoration = CeilingDecoration.objects.filter( uuid__in=ceiling_decoration_uuid)
            project_basic.ceiling_decoration.set(ceiling_decoration)
            
        if lighting_type_uuid:
            lighting_type = LightingType.objects.filter(uuid__in =lighting_type_uuid)
            project_basic.lighting_type.set(lighting_type)
            
        if wall_decoration_uuids:
            wall_decorations = WallDecorations.objects.filter(uuid__in=wall_decoration_uuids)
            project_basic.wall_decorations.set(wall_decorations)
            
        if flooring_material_uuid:
            flooring_material = FlooringMaterial.objects.filter(uuid__in=flooring_material_uuid)
            project_basic.flooring_material.set(flooring_material)
            
        if furniture_uuids:
            furniture = Furniture.objects.filter(uuid__in=furniture_uuids)
            project_basic.furniture.set(furniture)
            
        if clientOpenToMakeEdit:
            clientOpenToMakeEdit_ob = get_object_or_404(ClientOpenToMakeEdit, uuid=clientOpenToMakeEdit)
            project_basic.clientOpenToMakeEdit = clientOpenToMakeEdit_ob
        if Plumbing_established:
            Plumbing_established_ob = get_object_or_404(PlumbingEstablished, uuid=Plumbing_established)
            project_basic.plumbingEstablished = Plumbing_established_ob
        if Ceiling_gypsum_board:
            Ceiling_gypsum_board_ob = get_object_or_404(CeilingGypsumBoard, uuid=Ceiling_gypsum_board)
            project_basic.ceilingGypsumBoard = Ceiling_gypsum_board_ob
        if Door_provided:
            Door_provided_ob = get_object_or_404(DoorProvided, uuid=Door_provided)
            project_basic.doorProvided = Door_provided_ob
        if Ceramic_existed:
            Ceramic_existed_ob = get_object_or_404(CeramicExisted, uuid=Ceramic_existed)
            project_basic.ceramicExisted = Ceramic_existed_ob
            
        if toilet_type:
            toilet_type_ob = get_object_or_404(ToiletType, uuid=toilet_type)
            project_basic.toiletType = toilet_type_ob
            
        if heater:
            heater_ob = get_object_or_404(Heater, uuid=heater)
            project_basic.heater = heater_ob
            
        if hight_window:
            # hight_window = get_object_or_404(HightWindow, uuid=hight_window_uuid)
            project_basic.hight_window = hight_window
        if location:
            try:
                validate_google_maps_link(location)
            except:
                return Response({'error': 'Invalid Google Maps link'}, status=400)
        project_basic.location = location
        project_basic.dimensions = dimensions
        project_basic.meters = meters
        project_basic.is_add_fur_2d = is_add_fur_2d
        project_basic.is_boiler = is_boiler
        project_basic.count_boiler = count_boiler
        
        project_basic.save()
    except:
        return Response({'error': 'Invalid data or UUID'}, status=400)
    
    serializer = BasicProjectSerializer(project_basic)
    return Response(serializer.data, status=status.HTTP_200_OK)
class ProjectBasicListAPIView(APIView):
    def get(self, request):
        projects = ProjectBasic.objects.all()
        serializer = ProjectBasicSerializer(projects, many=True)
        return Response(serializer.data)
    
from rest_framework.parsers import MultiPartParser, FormParser
def handle_form_submission(request):
    if request.method == 'POST':
        project_uuid = request.POST.get('project_uuid')
        file = request.FILES.get('file')
        image = request.FILES.get('image')

        # Process the form data here
        # ...

        return HttpResponse("Form submission successful!")
    else:
        return HttpResponse("Invalid request method.")
from django.http import JsonResponse
def update_file(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        is_checked = request.POST.get('is_checked')
        print(request.POST)
        projectFile = ProjectFile.objects.get(uuid=file_id)
        if is_checked:
            projectFile.can_client_sea = True 
            projectFile.save()
        # Update the file data based on file_id and is_checked
        print(projectFile.can_client_sea)
        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # Return a JSON response indicating failure
    return JsonResponse({'success': False})


logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        project_uuid = request.POST.get('project_uuid')
        file_name = request.FILES.get('file_name')
        file_name_str = request.POST.get('file_name_str')

        if not project_uuid:
            return JsonResponse({'success': False, 'message': 'Project UUID is required.'})

        if not file_name:
            return JsonResponse({'success': False, 'message': 'File is required.'})

        project_basic = get_object_or_404(ProjectBasic, uuid=project_uuid)
        print("uploading >>>")
        try:
            project_file = ProjectFile.objects.create(
                project=project_basic.project,
                name=file_name_str,
                file=file_name,
            )
            print(project_file)
            project_file.save()
            print("uploaded")
            return JsonResponse({'success': True, 'message': 'File uploaded successfully!'})
        except Exception as e:
            logger.exception("An error occurred while creating the ProjectFile object. %s", e)
            return JsonResponse({'success': False, 'message': 'An error occurred while uploading the file.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
class ProjectUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        print(request.data.get('project_uuid'))
        project_id = request.data.get('project_uuid')
        file = request.FILES.get('file')
        image = request.FILES.get('image')
        print(project_id)
        # Save file and image to the project
        try:
            project = Project.objects.get(client__uuid=project_id)
            print(project)

            if file:
                existing_file = ProjectFile.objects.filter(project=project).first()
                if existing_file:
                    print(file.name,existing_file.file.name.split('/')[-1])
                    if existing_file and existing_file.file.name.split('/')[-1] == file.name and existing_file.file.size == file.size:
                        return Response({'error': 'File with the same name and size already exists in the project'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    project_file = ProjectFile(project=project, file=file)
                    project_file.save()
                    file_serializer = FileSerializer(project_file, context={'request': request})
                    file_data = file_serializer.data
                else :
                    existing_file = ProjectFile.objects.create(project=project)
                    print(file.name,existing_file.file.name.split('/')[-1])
                    if existing_file and existing_file.file.name.split('/')[-1] == file.name and existing_file.file.size == file.size:
                        return Response({'error': 'File with the same name and size already exists in the project'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    project_file = ProjectFile(project=project, file=file)
                    project_file.save()
                    file_serializer = FileSerializer(project_file, context={'request': request})
                    file_data = file_serializer.data
                
            else:
                file_data = None

            if image:
                existing_image = ProjectImage.objects.filter(project=project).first()
                if existing_image and existing_image.image.name == image.name and existing_image.image.size == image.size:
                    return Response({'error': 'Image with the same name and size already exists in the project'},
                                    status=status.HTTP_400_BAD_REQUEST)

                project_image = ProjectImage(project=project, image=image)
                project_image.save()
                image_serializer = ImageSerializer(project_image, context={'request': request})
                image_data = image_serializer.data
            else:
                image_data = None

            response_data = {
                'file': file_data,
                'image': image_data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import generics


class ProjectFileAPIView(generics.ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        project_uuid = self.request.data['project_uuid']
        return ProjectFile.objects.filter(project__client__uuid=project_uuid)
    
class ProjectImagesAPIView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        project_uuid = self.request.data['project_uuid']
        return ProjectImage.objects.filter(project__client__uuid=project_uuid)
    

from django.shortcuts import get_object_or_404

class ProjectFileDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        project_id = self.request.data['project_uuid']
        return ProjectFile.objects.filter(project__uuid=project_id)

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'uuid': self.request.data['file_uuid']}
        return get_object_or_404(queryset, **filter_kwargs)
class ProjectImageDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        project_id = self.request.data['project_uuid']
        return ProjectImage.objects.filter(project__uuid=project_id)

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'uuid': self.request.data['image_uuid']}
        return get_object_or_404(queryset, **filter_kwargs)
    


class ProjectStudyListCreateView(generics.ListCreateAPIView):
    queryset = ProjectStudy.objects.all()
    serializer_class = ProjectStudySerializer

class ProjectStudyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectStudy.objects.all()
    serializer_class = ProjectStudySerializer

class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    lookup_field = 'uuid'
    
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj
    def create(self, request, *args, **kwargs):
        project_study = request.data.get('project_study')
        project_study_id = get_object_or_404(ProjectStudy, uuid = project_study).id

        # Create a dictionary containing the data to be sent to the serializer
        data = {
            'project_study': project_study_id,
            'message': request.data.get('message'),
            'replies': request.data.get('replies'),
            # 'status': request.data.get('status'),
            'uuid': request.data.get('uuid')
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  # Updated lookup field

    # Rest of the code...
class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
class ProjectStudyAPIView(APIView):
    def get(self, request, project_study_uuid):
        try:
            project_study = ProjectStudy.objects.get(uuid=project_study_uuid)
            feedbacks = Feedback.objects.filter(project_study=project_study)

            project_study_serializer = ProjectStudySerializer(project_study)
            feedbacks_serializer = FeedbackSerializer(feedbacks, many=True)

            data = {
                'project_study': project_study_serializer.data,
                'feedbacks': feedbacks_serializer.data
            }

            return Response(data)
        except ProjectStudy.DoesNotExist:
            return Response({'error': 'Project Study not found'}, status=404)
from django.views import View

class FeedbackAPIView(View):
    def get(self, request):
        client_uuid = request.GET.get('client_uuid')
        project_uuid = request.GET.get('study_uuid')
        
        if not client_uuid or not project_uuid:
            return JsonResponse({'error': 'client_uuid and study_uuid are required'}, status=400)
        
        feedback = Feedback.objects.filter(
            project_study__project__client__uuid=client_uuid,
            project_study__uuid=project_uuid
        )
        feedback_list = [
            {
                'message': item.message,
                'status': item.status,
                'current_action': item.get_current_action(),
                'is_seen': item.is_seen,
                'created_at': item.created_at,
                'uuid': item.uuid,
                'replies':[{"reply":itemN,'owner':"SC"} for itemN in item.replies.all().values('message')]
            }
            for item in feedback
        ]
        
        if not feedback_list:
            return JsonResponse({'message': 'No feedback found'}, status=404)
        
        return JsonResponse({'feedback': feedback_list})
class ReplyListCreateView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
@api_view(['POST'])
def create_project_study(request, tech_uuid):
    try:
        technical = Technical.objects.get(uuid=tech_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Invalid Technical UUID'}, status=status.HTTP_400_BAD_REQUEST)
    
    client_uuid = request.data.get('client_uuid')
    if not client_uuid:
        return Response({'error': 'client_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    project_data = request.data.copy()
    project_data['project'] = Project.objects.get(client__uuid =client_uuid).id
    
    if request.method == 'POST':
        serializer = ProjectStudySerializer(data=project_data)
        if serializer.is_valid():
            project_study = serializer.save()
            return Response(ProjectStudySerializer(project_study).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['POST'])
def create_project_study_feeds(request, tech_uuid):
    try:
        technical = Technical.objects.get(uuid=tech_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Invalid Technical UUID'}, status=status.HTTP_400_BAD_REQUEST)
    
    client_uuid = request.data.get('client_uuid')
    if not client_uuid:
        return Response({'error': 'client_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
    client_study = request.data.get('client_study')
    if not client_study:
        return Response({'error': 'client_study is required'}, status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.get(client__uuid =client_uuid)
    study = ProjectStudy.objects.get(uuid = client_study)
    
    project_data = request.data.copy()
    project_data['project_study'] = study.id
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=project_data)
        if serializer.is_valid():
            project_study = serializer.save()
            return Response(FeedbackSerializer(project_study).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['POST'])
def create_project_study_feeds_reply(request, tech_uuid):
    try:
        technical = Technical.objects.get(uuid=tech_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Invalid Technical UUID'}, status=status.HTTP_400_BAD_REQUEST)
    
    client_uuid = request.data.get('client_uuid')
    if not client_uuid:
        return Response({'error': 'client_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
    client_feedback_uuid = request.data.get('client_feedback_uuid')
    if not client_feedback_uuid:
        return Response({'error': 'client_feedback_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
    feedback = Feedback.objects.get(uuid = client_feedback_uuid)
    
    project_data = request.data.copy()
    project_data['feedback'] = feedback.id
    if request.method == 'POST':
        reply_serializer = ReplySerializer(data=project_data)
        if reply_serializer.is_valid():
            reply_serializer.save()
            return Response(reply_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(reply_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['Get'])
def get_project_study(request, tech_uuid):
    try:
        technical = Technical.objects.get(uuid=tech_uuid)
    except Viewer.DoesNotExist:
        return Response({'error': 'Invalid Technical UUID'}, status=status.HTTP_400_BAD_REQUEST)
    
    client_uuid = request.data.get('client_uuid')
    if not client_uuid:
        return Response({'error': 'client_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    project = Project.objects.get(client__uuid =client_uuid)
    study = ProjectStudy.objects.filter(project = project)
    if request.method == 'GET':
        serializer = ProjectStudySerializer(study,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)