from django import forms
from .models import Category, EmployeeWebsite, Pic

class PicUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Pic
        fields = ('title', 'description', 'category', 'image')
        
        widgets = {
            'title': forms.TextInput(attrs={'nullable': True}),
            'description': forms.Textarea(attrs={'nullable': True}),
        }
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeWebsite
        fields = ('name', 'job_title', 'description', 'picture')