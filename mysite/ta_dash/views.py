from django.shortcuts import render
from models import UserProfile, Class, Enrollment, AccountProfileID, Assignment
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from forms import ClassForm, AssignmentForm

def retrieve_profile(user):
    profile_id = AccountProfileID.objects.get(id=user.accountprofileid.id).profileID
    user_profile = UserProfile.objects.get(id=profile_id)
    return user_profile
def check_enrollment(class_object, user_profile):
    selected_enrollment = Enrollment.objects.get(enrolled_class=class_object, user=user_profile)
    return selected_enrollment

def check_access(class_object, access):
    selected_enrollment = check_enrollment(class_object)
    if selected_enrollment:
        if selected_enrollment.access == access:
            return True
        else:
            return False
def handle_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
# Create your views here.
def list_view(request):
    if request.user.is_authenticated():
        result_list = []
        user_profile = retrieve_profile(request.user)
        enrolled_classes = user_profile.enrollment_set.all().values("user","enrolled_class")
        for element in enrolled_classes:
            result_list.append(Class.objects.get(id=element["enrolled_class"]))
        return HttpResponse(serialize('json', result_list))
    else:
        return HttpResponse("You need to log in")

def create_class(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            created_class = Class.objects.create(name=request.POST["name"])
            user_profile = retrieve_profile(request.user)
            created_enrollment = Enrollment.objects.create(enrolled_class=created_class, user=user_profile, access="TR")
            return HttpResponse("Object Created")
        else:
            form = ClassForm()
            return render(request, 'main/create.html', {"form": form})
    else:
        return HttpResponse("You need to log in")



def class_index(request):
    if request.user.is_authenticated():
        selected_class = Class.objects.get(id=request.post["class_id"])
        user_profile = retrieve_profile(request.user)
        if check_enrollment(selected_class, user_profile):
            return HttpResponse(selected_class)
        else:
            return HttpResponse("You do not have access to the class")
    else:
        return HttpResponse("Please log in")

def create_assignment(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            selected_class = Class.objects.get(id=request.post["class_id"])
            user_profile = retrieve_profile(request.user)
            if check_access(selected_class, "TR", user_profile):
                Assignment.objects.create(name=request.POST["assignment_name"], class_id=selected_class)
        else:
            form = AssignmentForm()
            return render(request, "main/create_assignment.html", {"form": form})
    else:
        return HttpResponse("You need to login")

def create_submission(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            selected_class = Class.objects.get(id=request.post["class_id"])
            user_profile = retrieve_profile(request.user)
            if check_access(selected_class, "ST", user_profile):
                selected_assignment = Assignment.objects.get(id=request.POST["assignment_id"])
                if request.POST["file"]:
                    handle_uploaded_file(request.FILES['file'])

                    Upload.objects.create(user=user_profile, assignment = selected_assignment, )
        else:
            form = AssignmentForm()
            return render(request, "main/create_assignment.html", {"form": form})
    else:
        return HttpResponse("You need to login")
            
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