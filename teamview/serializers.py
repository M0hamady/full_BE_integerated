from rest_framework import serializers
from teamview.models import Viewer



class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = ['name', 'uuid', 'is_active']