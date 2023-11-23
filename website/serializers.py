# serializers.py

from rest_framework import serializers
from .models import Category, EmployeeWebsite, Pic

class EmployeeWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWebsite
        fields = ['id', 'name', 'picture', 'job_title', 'description']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class PicSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Pic
        fields = ('title', 'description', 'category','image')