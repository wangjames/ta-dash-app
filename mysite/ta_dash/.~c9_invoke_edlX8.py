from django.shortcuts import render
from models import UserProfile, Class, Enrollment, AccountProfileID
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def list_view(request):
    if request.user.is_authenticated:
        result_list = []
        
        user = UserProfile.objects.get(name=request.user.username)
        enrolled_classes = user.enrollment_set.all().values("user","enrolled_class")
        for element in enrolled_classes:
            result_list.append(Class.objects.get(id=element["enrolled_class"]))
    else:
    else:
        return HttpResponse("You need to log in")
    
def register(request):
    if request.method == "POST":
        finished_form = UserCreationForm(request.POST)
        print request.POST
        print finished_form.errors
        if finished_form.is_valid():
            print "yup"
            finished_form.save()
            username = finished_form.cleaned_data.get('username')
            raw_password = finished_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        return HttpResponse("Finished.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html',{"form":form})