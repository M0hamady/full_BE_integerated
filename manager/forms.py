from django import forms
from django.contrib.auth.forms import UserCreationForm

from client.models import Client
from project.models import Project, ProjectBasic, ProjectStudy

from .models import User
from django.contrib.auth.forms import AuthenticationForm


class ProjectStudyForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ProjectStudy
        fields = '__all__'
        widgets = {
            'total_price': forms.NumberInput(attrs={'required': False})
        }

    def __init__(self, *args, **kwargs):
        current_project = kwargs.pop('current_project', None)
        super().__init__(*args, **kwargs)
        if current_project:
            self.fields['project'].initial = current_project
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-class','autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-class'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-class'}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-class', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my-class'}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'add_by',
            'name',
            'email',
            'number',
            'location',
            'locationLink',
            'coming_from',
            'is_active',
            'is_viewer_viewed',
            'date_viewer_viewed',
            'is_tech_viewed',
            'date_tech_viewed',
            'meeting_time',
            'contract_meeting_time',
            'is_meeting_approved',
            'is_contract_meeting_approved',
            'is_location_approved',
            'is_contract_location_approved',
            'is_contract_approved',
            'is_3d_design_approved',
            'is_client_project_finished',
            'is_Project_done',
            'notes_for_home',
            'preferred_license_method',
        ]
        widgets = {
            'is_active': forms.CheckboxInput(),
            'is_viewer_viewed': forms.CheckboxInput(),
            'is_tech_viewed': forms.CheckboxInput(),
            'is_meeting_approved': forms.CheckboxInput(),
            'is_contract_meeting_approved': forms.CheckboxInput(),
            'is_location_approved': forms.CheckboxInput(),
            'is_contract_location_approved': forms.CheckboxInput(),
            'is_contract_approved': forms.CheckboxInput(),
            'is_3d_design_approved': forms.CheckboxInput(),
            'is_client_project_finished': forms.CheckboxInput(),
            'is_Project_done': forms.CheckboxInput(),
            'meeting_time': forms.DateTimeInput(attrs={'class': 'datetimepicker-input'}),
            'contract_meeting_time': forms.DateTimeInput(attrs={'class': 'datetimepicker-input'}),
        }
from django.utils.safestring import mark_safe
from colorfield.fields import ColorWidget
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from colorfield.fields import ColorWidget
class ColorPickerWidget(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs, )
        rendered = super().render(name, value, final_attrs, renderer)
        script = '''
        <script>
        $(function() {
            $('#id_{0}').spectrum({{
                preferredFormat: "hex",
                showInput: true,
                showInitial: true,
                showPalette: true,
                palette: [
                    ["#ff0000", "#00ff00", "#0000ff"],
                    ["#ffff00", "#00ffff", "#ff00ff"],
                    ["#000000", "#ffffff"]
                ]
            }});
        });
        </script>
        '''.format(final_attrs['id'])
        return mark_safe(rendered + script)
class Profile_project_UpdateForm(forms.ModelForm):
    # design_colors = forms.CharField(widget=ColorPickerWidget)
    class Meta:
        model = ProjectBasic
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(Profile_project_UpdateForm, self).__init__(*args, **kwargs)

            # Iterate over each field in the form and set its required attribute to False
            widgets = {
                'project': forms.Select(attrs={'class': 'form-control'}),
                'location': forms.TextInput(attrs={'class': 'form-control'}),
                'dimensions': forms.TextInput(attrs={'class': 'form-control'}),
                'meters': forms.NumberInput(attrs={'class': 'form-control'}),
                'design_styles': forms.CheckboxSelectMultiple(),
                'ceiling_decoration': forms.CheckboxSelectMultiple(),
                'lighting_type': forms.CheckboxSelectMultiple(),
                'wall_decorations': forms.CheckboxSelectMultiple(),
                'flooring_material': forms.CheckboxSelectMultiple(),
                'furniture': forms.CheckboxSelectMultiple(),
                'hight_window': forms.TextInput(attrs={'class': 'form-control'}),
                'clientOpenToMakeEdit': forms.Select(attrs={'class': 'form-control'}),
                'plumbingEstablished': forms.Select(attrs={'class': 'form-control'}),
                'ceilingGypsumBoard': forms.Select(attrs={'class': 'form-control'}),
                'doorProvided': forms.Select(attrs={'class': 'form-control'}),
                'ceramicExisted': forms.Select(attrs={'class': 'form-control'}),
                'toiletType': forms.Select(attrs={'class': 'form-control'}),
                'heater': forms.Select(attrs={'class': 'form-control'}),
                'is_add_fur_2d': forms.CheckboxInput(),
                'is_boiler': forms.CheckboxInput(),
                'count_boiler': forms.NumberInput(attrs={'class': 'form-control'}),
                'count_kids': forms.NumberInput(attrs={'class': 'form-control'}),
                'count_kids_male': forms.NumberInput(attrs={'class': 'form-control'}),
                'count_kids_female': forms.NumberInput(attrs={'class': 'form-control'}),
            }
            # Define fields variable
            # Add required=False to all fields
            for field in self.fields:
                self.fields[field].required = False
                self.fields[field].null = False
            fields.update(field_widgets)