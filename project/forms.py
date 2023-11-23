from django import forms
from multiselectfield import MultiSelectFormField

class ColorChoicesWidget(forms.CheckboxSelectMultiple):
    template_name = 'admin/color_choices_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Add custom CSS classes or attributes to the widget if needed
        return context

class ColorChoicesFormField(MultiSelectFormField):
    widget = ColorChoicesWidget

    def prepare_value(self, value):
        if value is None:
            return []
        return value

    def clean(self, value):
        if not value:
            return []
        return super().clean(value)