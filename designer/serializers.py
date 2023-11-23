from rest_framework import serializers
from .models import ChatBoot, Designer

class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = ('id', 'name',"uuid")
class ChatBootSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBoot
        fields = "__all__"