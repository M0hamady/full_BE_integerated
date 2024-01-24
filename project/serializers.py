import re
from client.models import *
from client.serializers import ClientSerializer
from designer.models import Designer
from designer.serializers import DesignerSerializer
from project.models import *
from rest_framework import serializers
from django.core.exceptions import ValidationError

import uuid

from teamview.models import Viewer
from technical.models import Technical

class ProjectImage2DSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    class Meta:
        model = ProjectImage2D
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')

    def create(self, validated_data):
        image = validated_data.pop('image')
        project_image = ProjectImage2D.objects.create(image=image, **validated_data)
        return project_image
    def get_project(self,obj):
        return obj.project.uuid
    def get_client(self,obj):
        return obj.project.client.uuid
class ReplyImage2DSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    class Meta:
        model = ReplyCommentImage2D
        fields = ('uuid', 'comment', 'text', 'created_at')
    def get_comment(self,obj):
        return obj.comment.uuid

class CommentImage2DSerializer(serializers.ModelSerializer):
    replies = ReplyImage2DSerializer(many=True, read_only=True)
    project_image = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentImage2D
        fields = ('uuid', 'project_image', 'text', 'created_at', 'replies')
    def get_project_image(self,obj):
        return obj.project_image.uuid
    

class FeedbackFloorSerializer(serializers.ModelSerializer):
    floor_uuid = serializers.UUIDField(write_only=True)  # Added field for floor UUID
    floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all(), required=False)
    class Meta:
        model = FeedbackFloor
        fields = ['id', 'floor', 'message', 'status', 'uuid', 'is_accepted', 'is_seen', 'floor_uuid']
        read_only_fields = ['uuid']
    def validate(self, attrs):
        if 'floor_uuid' in attrs and 'floor' in attrs:
            raise serializers.ValidationError("Both floor and floor_uuid cannot be provided at the same time.")
        return attrs
    def create(self, validated_data):
        floor_uuid = validated_data.pop('floor_uuid')
        try:
            floor = Floor.objects.get(uuid=floor_uuid)
        except Floor.DoesNotExist:
            raise serializers.ValidationError("Invalid floor UUID")
        validated_data['floor'] = floor
        return super().create(validated_data)
class WallDecorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallDecorations
        fields = '__all__'

class DesignStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignStyle
        fields = '__all__'

class CeilingDecorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeilingDecoration
        fields = '__all__'

class LightingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightingType
        fields = '__all__'

class DesignColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignColors
        fields = '__all__'
    def validate_name(self, value):
        # Validate the color format
        if not re.match(r'^#[0-9a-fA-F]{6}$', value):
            raise serializers.ValidationError('Invalid color format. Color should be in hexadecimal format, e.g., #454545.')
        

        return value
class FlooringMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringMaterial
        fields = '__all__'

class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = '__all__'

class HighWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = HightWindow
        fields = '__all__'
class ClientOpenToMakeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOpenToMakeEdit
        fields = '__all__'
class PlumbingEstablishedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlumbingEstablished
        fields = '__all__'
class CeilingGypsumBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeilingGypsumBoard
        fields = '__all__'
class DoorProvidedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorProvided
        fields = '__all__'
class CeramicExistedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeramicExisted
        fields = '__all__'
class ToiletTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToiletType
        fields = '__all__'
class HeaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heater
        fields = '__all__'
class NotesSerializer(serializers.ModelSerializer):
    project_basic = serializers.SerializerMethodField()
    class Meta:
        model = Notes
        fields = ['id', 'text', 'created_at', 'created_by','project_basic']
        read_only_fields = ['id', 'created_at','project_basic']

    def get_project_basic(self,obj):
        project = ProjectSerializer_client(obj.project_basic.project).data['name']
        return project
class CommentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=False, allow_null=True)
    designer = serializers.PrimaryKeyRelatedField(queryset=Designer.objects.all(), required=False, allow_null=True)
    viewer = serializers.PrimaryKeyRelatedField(queryset=Viewer.objects.all(), required=False, allow_null=True)
    technical = serializers.PrimaryKeyRelatedField(queryset=Technical.objects.all(), required=False, allow_null=True)
    parent = serializers.PrimaryKeyRelatedField(queryset='self', required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'project', 'content', 'can_client_see', 'client', 'parent', 'designer', 'viewer', 'technical', 'uuid']

    def validate(self, data):
        if data['client'] and (data['designer'] or data['viewer'] or data['technical']):
            raise ValidationError('A comment can only be assigned to one client at a time')
        return data

class ProjectBasicSerializer(serializers.ModelSerializer):
    design_styles = serializers.PrimaryKeyRelatedField(queryset=DesignStyle.objects.all(), many=True)
    design_colors = serializers.PrimaryKeyRelatedField(queryset=DesignColors.objects.all(), many=True)
    ceiling_decoration = serializers.PrimaryKeyRelatedField(queryset=CeilingDecoration.objects.all(), many=True)
    lighting_type = serializers.PrimaryKeyRelatedField(queryset=LightingType.objects.all(), many=True)
    wall_decorations = serializers.PrimaryKeyRelatedField(queryset=WallDecorations.objects.all(), many=True)
    flooring_material = serializers.PrimaryKeyRelatedField(queryset=FlooringMaterial.objects.all(), many=True)
    furniture = serializers.PrimaryKeyRelatedField(queryset=Furniture.objects.all(), many=True)
    hight_window = serializers.PrimaryKeyRelatedField(queryset=HightWindow.objects.all(), required=False, allow_null=True)

    class Meta:
        model = ProjectBasic
        fields = ['id', 'project', 'location', 'dimensions', 'meters', 'design_styles', 'design_colors', 'ceiling_decoration', 'lighting_type', 'wall_decorations', 'flooring_material', 'furniture', 'hight_window', 'is_add_fur_2d', 'is_boiler', 'count_boiler', 'uuid']
        extra_kwargs = {
            'location': {'required': True},
            'dimensions': {'required': True},
            'meters': {'required': True},
            'hight_window': {'required': True},
            'is_add_fur_2d': {'required': True},
            'is_boiler': {'required': True},
            'count_boiler': {'required': True},

        }
    def validate(self, data):
        if data['is_add_fur_2d'] and not data['furniture']:
            raise ValidationError('Furniture is required if is_add_fur_2d is True')
        return data


class ProjectFileSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectFile
        fields = ['id', 'project', 'name', 'file', 'uuid', 'can_client_see']

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise ValidationError('File must be a PDF')
        return value

class ProjectImageSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectImage
        fields = ['id', 'project', 'name', 'image', 'uuid', 'can_client_see']

    def validate_image(self, value):
        if not value.name.endswith('.jpg') and not value.name.endswith('.jpeg') and not value.name.endswith('.png') and not value.name.endswith('.gif'):
            raise ValidationError('Image must be a JPEG, PNG, or GIF')
        return value

class ProjectDetailsSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectDetails
        fields = ['id', 'project', 'colors', 'uuid', 'can_client_see']



class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'client', 'uuid', 'assign_to_2d_designer', 'assign_to_3d_designer',
                  'viewer', 'technical_user')

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        client = Client.objects.create(**client_data)
        project = Project.objects.create(client=client, **validated_data)
        return project
class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'client', 'uuid', 'assign_to_2d_designer', 'assign_to_3d_designer',
                  'viewer', 'technical_user','is_client_approved_study','is_client_approved_2d','is_client_approved_3d')

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        client = Client.objects.create(**client_data)
        project = Project.objects.create(client=client, **validated_data)
        return project
class ProjectSerializer_client(serializers.ModelSerializer):
    is_assigned_to_2d = serializers.SerializerMethodField()
    is_assigned_to_3d = serializers.SerializerMethodField()
    assign_to_2d_designer = serializers.SerializerMethodField()
    assign_to_3d_designer = serializers.SerializerMethodField()
    project_works_percentage = serializers.SerializerMethodField()
    basic_data_percentage = serializers.SerializerMethodField()
    roadmap = serializers.SerializerMethodField()
    budget = serializers.SerializerMethodField()
    study = serializers.SerializerMethodField()
    client_pics =  serializers.SerializerMethodField()
    client_license =  serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields ='__all__'

    def get_is_assigned_to_2d(self,obj):
        return obj.is_assigned_to_2d
    def get_client_license(self,obj):
        return obj.client.uuid
    def get_client_pics(self,obj):
        images = ProjectImage.objects.filter(project= obj)
        list_url = []
        for image in images:
            list_comments = []

            comments = Comment_image.objects.filter(image__uuid = image.uuid)
            for comment in comments:
                list_comments.append({
                    "comment":str(comment.content),
                    "uuid":str(comment.uuid),
                    "parent":str(comment.parent),
                    "owner":str(comment.owner),
                    "created_at":str(comment.created_at)
                })
            list_url.append({"image":image.image.url,"uuid":image.uuid,"name":image.name,'comments':list_comments})
            

        return list_url
    def get_assign_to_2d_designer(self,obj):
        return DesignerSerializer(obj.assign_to_2d_designer).data
    def get_assign_to_3d_designer(self,obj):
        if obj.assign_to_3d_designer:
            return DesignerSerializer(obj.assign_to_3d_designer).data
        else: return None
    def get_is_assigned_to_3d(self,obj):
        return obj.is_assigned_to_3d
    def get_project_works_percentage(self,obj):
        return obj.project_works_percentage
    def get_basic_data_percentage(self,obj):
        return obj.basic_data_percentage
    def get_roadmap(self,obj):
        return obj.roadmap
    def get_budget(self,obj):
        total_budjet = 0
        for moshtra in obj.roadmap:
            total_budjet += moshtra['moshtrayat_budget']
        return total_budjet
    def get_study(self,obj):
        return obj.study
class BasicProjectSerializer(serializers.ModelSerializer):
    # design_styles = serializers.SerializerMethodField()
    project__uuid = serializers.SerializerMethodField()
    design_colors = serializers.SerializerMethodField()
    design_styles = serializers.SerializerMethodField()
    ceiling_decoration = serializers.SerializerMethodField()
    lighting_type = serializers.SerializerMethodField()
    wall_decorations = serializers.SerializerMethodField()
    flooring_material = serializers.SerializerMethodField()
    furniture = serializers.SerializerMethodField()
    hight_window = serializers.SerializerMethodField()
    clientOpenToMakeEdit = serializers.SerializerMethodField()
    Plumbing_established = serializers.SerializerMethodField()
    Ceiling_gypsum_board = serializers.SerializerMethodField()
    Door_provided = serializers.SerializerMethodField()
    Ceramic_existed = serializers.SerializerMethodField()
    toilet_type = serializers.SerializerMethodField()
    heater = serializers.SerializerMethodField()
    # comments_options = serializers.SerializerMethodField()
    client_project_data = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectBasic
        fields ='__all__'
    def get_comments_options(self, obj):
        images = CommentOptions.objects.filter(project_basic = obj , parent = None)
        images_serializers = CommentOptionsSerializer(images, many = True)

        return images_serializers.data
    def get_comments_by_key_option(self,key_option, data):
        comments = []
        for item in data:
            if item["Key_option"] == key_option:
                comments.append(item["comment"])
        return comments
    def get_client_project_data(self,obj):
        comments = CommentOptions.objects.filter(project_basic = obj , parent = None)
        comment_options_serializer = CommentOptionsSerializer(comments, many = True)
        res = []
        
        if DesignStyleSerializer(obj.design_styles,many= True).data:
            res.append({
                "title":"design_styles",
                'answers':DesignStyleSerializer(obj.design_styles,many= True).data,
                'comments':self.get_comments_by_key_option("design_styles",comment_options_serializer.data)
            })
        if DesignColorsSerializer(obj.design_colors,many= True).data:
            res.append({
                "title":"design_colors",
                'answers':DesignColorsSerializer(obj.design_colors,many= True).data,
                'comments':self.get_comments_by_key_option("design_styles",comment_options_serializer.data)

                
            })
        if DesignStyleSerializer(obj.design_styles,many= True).data:
                res.append({
                "title":"ceiling_decoration",
                'answers':DesignStyleSerializer(obj.design_styles,many= True).data,
                'comments':self.get_comments_by_key_option("ceiling_decoration",comment_options_serializer.data)

                    })
                
        if LightingTypeSerializer(obj.lighting_type,many= True).data:
            res.append({
                "title":"lighting_type",
                'answers':LightingTypeSerializer(obj.lighting_type,many= True).data,
                'comments':self.get_comments_by_key_option("lighting_type",comment_options_serializer.data)

            })
            
        if  FlooringMaterialSerializer(obj.flooring_material,many= True).data:
            res.append({
                "title":"flooring_material",
                'answers':FlooringMaterialSerializer(obj.flooring_material,many= True).data,
                'comments':self.get_comments_by_key_option("flooring_material",comment_options_serializer.data)

            })
            
        if  FurnitureSerializer(obj.furniture,many= True).data:
            res.append({
                "title":"furniture",
                'answers':FurnitureSerializer(obj.furniture,many= True).data,
                'comments':self.get_comments_by_key_option("furniture",comment_options_serializer.data)

            })
            
        if obj.hight_window:
            res.append({
                "title":"hight_window",
                'answers':[{
                    "id": 1,
                    "name": [f'{obj.hight_window}'],
                    "uuid": "ab516db0-6529-488d-ad85-448ca4fae416"
                },]
                ,
                'comments':self.get_comments_by_key_option("furniture",comment_options_serializer.data)

            })
           
        if ClientOpenToMakeEditSerializer( obj.clientOpenToMakeEdit).data['name']:
            res.append([{
                "title":"clientOpenToMakeEdit",
                'answers':[ClientOpenToMakeEditSerializer( obj.clientOpenToMakeEdit).data],
                'comments':self.get_comments_by_key_option("clientOpenToMakeEdit",comment_options_serializer.data)

            }])
        if PlumbingEstablishedSerializer( obj.plumbingEstablished).data['name']:
            res.append([
            {
                "title":"Plumbing_established",
                'answers':[PlumbingEstablishedSerializer( obj.plumbingEstablished).data],
                'comments':self.get_comments_by_key_option("Plumbing_established",comment_options_serializer.data)

            }]),
            if DoorProvidedSerializer( obj.doorProvided).data['name']:
                res.append([{
                "title":"Door_provided",
                'answers':[DoorProvidedSerializer( obj.doorProvided).data],
                'comments':self.get_comments_by_key_option("Door_provided",comment_options_serializer.data)

                }])
                
            if  CeramicExistedSerializer( obj.ceramicExisted).data['name']:
                res.append([{
                "title":"Ceramic_existed",
                'answers':[CeramicExistedSerializer( obj.ceramicExisted).data],
                'comments':self.get_comments_by_key_option("Ceramic_existed",comment_options_serializer.data)

            }])
            if  ToiletTypeSerializer( obj.toiletType).data['name']:
                res.append([{
                "title":"toilet_type",
                'answers':[ToiletTypeSerializer( obj.toiletType).data],
                'comments':self.get_comments_by_key_option("toilet_type",comment_options_serializer.data)

            }])
            if  HeaterSerializer( obj.heater).data['name']:
                res.append([{
                "title":"heater",
                'answers':[HeaterSerializer( obj.heater).data],
                'comments':self.get_comments_by_key_option("heater",comment_options_serializer.data)

            }])
            if  WallDecorationSerializer( obj.heater).data['name']:
                res.append([{
                "title":"wall_decorations",
                'answers':[WallDecorationSerializer( obj.heater).data],
                'comments':self.get_comments_by_key_option("wall_decorations",comment_options_serializer.data)

            }])
        
        return res
    # def get_design_styles(self,obj):
    #       return DesignStyleSerializer(obj.design_styles,many= True).data
    def get_design_colors(self,obj):
          return DesignColorsSerializer(obj.design_colors,many= True).data
    def get_design_styles(self,obj):
          return DesignStyleSerializer(obj.design_styles,many= True).data
    def get_ceiling_decoration(self,obj):
          return CeilingDecorationSerializer(obj.ceiling_decoration,many= True).data
    def get_lighting_type(self,obj):
          return CeilingDecorationSerializer(obj.lighting_type,many= True).data
    def get_wall_decorations(self,obj):
          return WallDecorationSerializer(obj.wall_decorations,many= True).data
    def get_flooring_material(self,obj):
          return FlooringMaterialSerializer(obj.flooring_material,many= True).data
    def get_furniture(self,obj):
          return FurnitureSerializer(obj.furniture,many= True).data
    def get_project__uuid(self,obj):
          return obj.project.uuid
    def get_hight_window(self,obj):
          try:
            return obj.hight_window + ": meter"
          except: return ""
    def get_clientOpenToMakeEdit(self,obj):
          try:
            return ClientOpenToMakeEditSerializer( obj.clientOpenToMakeEdit).data
          except: return ""
    def get_Plumbing_established(self,obj):
          try:
            return PlumbingEstablishedSerializer( obj.plumbingEstablished).data
          except: return ""
    def get_Ceiling_gypsum_board(self,obj):
          try:
            return CeilingGypsumBoardSerializer( obj.ceilingGypsumBoard).data
          except: return ""
    def get_Door_provided(self,obj):
          try:
            return DoorProvidedSerializer( obj.doorProvided).data
          except: return ""
    def get_Ceramic_existed(self,obj):
          try:
            return CeramicExistedSerializer( obj.ceramicExisted).data
          except: return ""
    def get_toilet_type(self,obj):
          try:
            return ToiletTypeSerializer( obj.toiletType).data
          except: return ""
    def get_heater(self,obj):
          try:
            return HeaterSerializer( obj.heater).data
          except: return ""



class FileSerializer(serializers.ModelSerializer):
    file_link = serializers.SerializerMethodField()

    class Meta:
        model = ProjectFile
        fields = ('id', 'file', 'file_link','uuid','can_client_sea')


    def get_file_link(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url') and request is not None:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url
   

class CommentImageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Comment_image
        fields = ('id', 'image', 'content', 'client', 'parent', 'designer', 'viewer', 'technical', 'uuid', 'replies')
    def get_image(self,obj):
        return obj.image.uuid
    def get_replies(self, obj):
        replies = Comment_image.objects.filter(parent=obj)
        replies
        serializer = self.__class__(replies, many=True)
        if obj.is_reply:
            return serializer.data
        return []

class CommentOptionsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = CommentOptions
        fields = ('id', 'project_basic','Key_option','parent', 'comment', 'created_by','uuid', 'replies')

    def get_replies(self, obj):
        replies = CommentOptions.objects.filter(parent=obj)
        replies
        serializer = self.__class__(replies, many=True)
        if obj.is_reply:
            return serializer.data
        return []


class ImageSerializer(serializers.ModelSerializer):
    image_link = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    # comments = CommentImageSerializer(many=True, read_only=True, source='comment_image_set')

    class Meta:
        model = ProjectImage
        fields = ('id', 'image', 'image_link', 'uuid', 'can_client_sea', 'comments')

    def get_image_link(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url') and request is not None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
    def get_comments(self, obj):
        images = Comment_image.objects.filter(image = obj)
        images_serializers = CommentImageSerializer(images, many = True)

        return images_serializers.data

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

    

class FeedbackSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = '__all__'
    def get_replies(self,obj):
        return ReplySerializer(Reply.objects.filter(feedback__uuid= obj.uuid),many = True).data
class ProjectStudySerializer(serializers.ModelSerializer):
    feedback_client = serializers.SerializerMethodField()

    class Meta:
        model = ProjectStudy
        fields = '__all__'



    def get_feedback_client(self,obj):
        return FeedbackSerializer(Feedback.objects.filter(project_study__uuid= obj.uuid),many = True).data