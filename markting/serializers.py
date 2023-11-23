from markting.models import Marketing
from rest_framework import serializers
class MarktingSerializer(serializers.ModelSerializer):
    count_added_user = serializers.SerializerMethodField()
    class Meta:
        model = Marketing
        fields = '__all__'
        

    def get_count_added_user(self,obj):
        return obj.count_added_user()