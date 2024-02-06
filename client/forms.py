from django import forms
from django.forms import formset_factory
from django.forms.models import BaseModelFormSet

from project.models import Project, ProjectBasic

from .models import Client, ClientAction

class ActionForm(forms.Form):
    ACTION_CHOICES = [
        ('searching', 'Searching for services'),
        ('future', 'Interested in future services'),
        ('working', 'Considering working with us')
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES)

class NotesForm(forms.ModelForm):
    class Meta:
        model = ClientAction
        fields = ('notes',)
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class BaseNotesFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = ClientAction.objects.none()

NotesFormSet = formset_factory(NotesForm, formset=BaseNotesFormSet, extra=1)

class ClientProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'number', 'location']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'number': 'Phone Number',
            'location': 'City',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }


class ProjectBasicUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectBasic
        fields = ['location', 'meters', 'count_family', 'count_kids_male', 'count_kids_female', 'count_rooms',
                  'furniture', 'count_boiler', 'heater', 'count_airconditioning', 'electronics_kitchen',
                  'ceilingGypsumBoard', 'lighting_type', 'toiletType', 'ceramicExisted']

        labels = {
            'location': 'Location ',
            'meters': 'Meters ',
            'count_family': 'Family Count ',
            'count_kids_male': 'Male Kids Count ',
            'count_kids_female': 'Female Kids Count ',
            'count_rooms': 'Rooms Count ',
            'furniture': 'Furniture ',
            'count_boiler': 'Boiler Count ',
            'heater': 'Heater ',
            'count_airconditioning': 'Air Conditioning Count ',
            'electronics_kitchen': 'Kitchen Electronics ',
            'ceilingGypsumBoard': 'Ceiling Gypsum Board ',
            'lighting_type': 'Lighting Type ',
            'toiletType': 'Toilet Type ',
            'ceramicExisted': 'Ceramic Existed ',
            # 'design_colors': 'Design Colors ',
        }

        placeholders = {
            'location': 'Location Placeholder',
            'meters': 'Meters Placeholder',
            'count_family': 'Family Count Placeholder',
            'count_kids_male': 'Male Kids Count Placeholder',
            'count_kids_female': 'Female Kids Count Placeholder',
            'count_rooms': 'Rooms Count Placeholder',
            'furniture': 'Furniture Placeholder',
            'count_boiler': 'Boiler Count Placeholder',
            'heater': 'Heater Placeholder',
            'count_airconditioning': 'Air Conditioning Count Placeholder',
            'electronics_kitchen': 'Kitchen Electronics Placeholder',
            'ceilingGypsumBoard': 'Ceiling Gypsum Board Placeholder',
            'lighting_type': 'Lighting Type Placeholder',
            'toiletType': 'Toilet Type Placeholder',
            'ceramicExisted': 'Ceramic Existed Placeholder',
            # 'design_colors': 'Design Colors Placeholder',
        }

        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'meters': forms.NumberInput(attrs={'class': 'form-control'}),
            'count_family': forms.NumberInput(attrs={'class': 'form-control'}),
            'count_kids_male': forms.NumberInput(attrs={'class': 'form-control'}),
            'count_kids_female': forms.NumberInput(attrs={'class': 'form-control'}),
            'count_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'furniture': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'count_boiler': forms.NumberInput(attrs={'class': 'form-control'}),
            'heater': forms.Select(attrs={'class': 'form-control'}),
            'count_airconditioning': forms.NumberInput(attrs={'class': 'form-control'}),
            'electronics_kitchen': forms.Select(attrs={'class': 'form-control'}),
            'ceilingGypsumBoard': forms.Select(attrs={'class': 'form-control'}),
            'lighting_type': forms.Select(attrs={'class': 'form-control'}),
            'toiletType': forms.Select(attrs={'class': 'form-control'}),
            'ceramicExisted': forms.Select(attrs={'class': 'form-control'}),
            # 'design_colors': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }