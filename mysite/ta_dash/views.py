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
    result_list = []
    user = UserProfile.objects.get(name="Jack")
    enrolled_classes = user.enrollment_set.all().values("user","enrolled_class")
    for element in enrolled_classes:
        result_list.append(Class.objects.get(id=element["enrolled_class"]))
    return HttpResponse(serialize('json', result_list))
    
def create_user(request):
    try:
        username = request.POST["user"]
        password = request.POST["password"]
        email = request.POST["email"]
        profile = UserProfile.objects.create(user=username)
        user = User.objects.create_user(username, email, password)
        AccountProfileID.objects.create(userID=user, profileID=profile.id)
    except:
        return HttpResponse("Failure")
    else:
        return HttpResponse("Completed")

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