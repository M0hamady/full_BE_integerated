from rest_framework import serializers
from .models import *



class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technical
        fields = ['name', 'uuid', 'is_active']