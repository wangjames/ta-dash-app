from django.forms import ModelForm, EmailField, Form, CharField
from ta_dash.models import Class, Assignment, Meeting
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import DateTimeInput
# Create the form class.
class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name']
class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields= ['assignment_name']

class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True,
        help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
class PendingEnrollmentForm(Form):
    email = EmailField(label="Recipient's Email")
class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ("address", "meeting_date")