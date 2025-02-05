# resume_upload/forms.py
from django import forms
from .models import Resume
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'email', 'resume_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Start Interview'))