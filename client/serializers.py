import datetime
import re
from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    data_percentage = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = '__all__'

        extra_kwargs = {
            'num': {'required': True},
            'name': {'required': True},
            'location': {'required': True},
            'coming_from': {'required': True},
        }
    def get_data_percentage(self,obj):
        return int(obj.calculate_data_completion_percentage2())
  
    def validate_number(self, value):
        # Perform professional validation on the number field
        # Example validation: Ensure the number is not blacklisted
        
        if not value.startswith('0'):
            value = '0' + value
        blacklist = ['01234567890', '09876543210']
        if value in blacklist:
            raise serializers.ValidationError("This phone number is not allowed.")
        return value

    def validate(self, attrs):
        # Perform professional validation across multiple fields
        # Example validation: Ensure the name and location are not the same
        name = attrs.get('name')
        location = attrs.get('location')
        if name and location and name.lower() == location.lower():
            raise serializers.ValidationError("The name and location cannot be the same.")

        # Update the date_viewer_viewed and date_tech_viewed fields
        if attrs.get('is_viewer_viewed'):
            attrs['date_viewer_viewed'] = datetime.datetime.now()
        if attrs.get('is_tech_viewed'):
            attrs['date_tech_viewed'] = datetime.datetime.now()

        return attrs
class ClientUpdateSerializer(serializers.ModelSerializer):
    data_percentage = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
        }

        
    def get_data_percentage(self,obj):
        return obj.calculate_data_completion_percentage2()
    def validate_number(self, value):
        # Perform professional validation on the number field
        # Example validation: Ensure the number is not blacklisted
        
        if not value.startswith('0'):
            value = '0' + value
        blacklist = ['01234567890', '09876543210']
        if value in blacklist:
            raise serializers.ValidationError("This phone number is not allowed.")
        return value

    def validate(self, attrs):
        # Perform professional validation across multiple fields
        # Example validation: Ensure the name and location are not the same
        name = attrs.get('name')
        location = attrs.get('location')
        if name and location and name.lower() == location.lower():
            raise serializers.ValidationError("The name and location cannot be the same.")

        # Update the date_viewer_viewed and date_tech_viewed fields
        if attrs.get('is_viewer_viewed'):
            attrs['date_viewer_viewed'] = datetime.datetime.now()
        if attrs.get('is_tech_viewed'):
            attrs['date_tech_viewed'] = datetime.datetime.now()

        return 
    
from django.core.validators import RegexValidator

class ClientRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    number = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^\+\d{1,3}-\d{9,15}$',
            message="Phone number must be entered in the format: '+{country code}-{number}'. Up to 15 digits allowed."
        )
    ])

    def create(self, validated_data):
        phone_number = validated_data['number']
        country_code, number = self.extract_country_code_and_number(phone_number)
        print(number, country_code)
        if country_code == '+2' and len(number) != 11:  
            raise serializers.ValidationError({"number": "For country code +2, the number must be exactly 11 digits long.","message":"incorrect number"})
        # Create the client object
        client = Client.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            number=number,
            # country_code=country_code
        )
        return client

    def extract_country_code_and_number(self, phone_number):
        # Extract the country code and number from the phone number
        match = re.search(r'^\+(\d{1,3})-(\d+)$', phone_number)
        if match:
            country_code = '+' +match.group(1)
            number = match.group(2)
            return country_code, number
        return None, None

class ClientAPI:
    def get_client_by_uuid(self, uuid):
        try:
            client = Client.objects.get(uuid=uuid)
            serializer = ClientSerializer(client)
            return serializer.data
        except Client.DoesNotExist:
            return None

    def register_client(self, name, email, number):
        client_data = {
            'name': name,
            'email': email,
            'number': number
        }
        serializer = ClientRegistrationSerializer(data=client_data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        return client
    


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    message = serializers.CharField()


class ClientWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
    def get_project_client(self, instance):
        project = instance.project_client()
        if project is not None:
            return project.id
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['project_client'] = self.get_project_client(instance)
        representation['action_needed'] = instance.action_needed()
        representation['data_completion_percentage'] = instance.calculate_data_completion_percentage2()

        if not instance.mobile and not instance.email:
            representation['error'] = 'Mobile or email is required'
        
        return representation