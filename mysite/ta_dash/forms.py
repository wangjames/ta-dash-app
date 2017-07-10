from django.forms import ModelForm
from models import Class, Assignment

# Create the form class.
class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name']
class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields= ['assignment_name']
