from django.shortcuts import render
from models import UserProfile, Class, Enrollment, AccountProfileID, Assignment, TextSubmission, Upload
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from forms import ClassForm, AssignmentForm

def returnAuthenticationStatus(request):
    if request.user.is_authenticated():
        return True
    else:
        return False
    
def retrieve_profile(request):

    if request.user:
        user = request.user
        profile_id = AccountProfileID.objects.get(id=user.accountprofileid.id).profileID
        user_profile = UserProfile.objects.get(id=profile_id)
        return user_profile
    else:
        return None

def check_enrollment(class_object, user_profile):
    selected_enrollment = Enrollment.objects.get(enrolled_class=class_object, user=user_profile)
    return selected_enrollment

def check_access(class_object, access, user_profile):
    selected_enrollment = check_enrollment(class_object, user_profile)
    if selected_enrollment:
        if selected_enrollment.access == access:
            return True
        else:
            return False

# Create your views here.
def list_view(request):
    if returnAuthenticationStatus(request):
        result_list = []
        create_class_url = "/main/create"
        user_profile = retrieve_profile(request)
        enrolled_classes = user_profile.enrollment_set.all().values("user","enrolled_class")
        for element in enrolled_classes:
            context_object = {}
            context_object["url"] =  "/main/class/" + str(element["enrolled_class"])
            context_object["name"] = Class.objects.get(id=element["enrolled_class"]).name
            result_list.append(context_object)
        return render(request, "main/index.html", {"class_list": result_list, "create_class_url": create_class_url})
    else:
        return HttpResponse("You need to log in")
def create_class(request):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            created_class = Class.objects.create(name=request.POST["name"])
            user_profile = retrieve_profile(request)
            created_enrollment = Enrollment.objects.create(enrolled_class=created_class, user=user_profile, access="TR")
            return HttpResponse("Object Created")
        else:
            form = ClassForm()
            return render(request, 'main/create.html', {"form": form})
    else:
        return HttpResponse("You need to log in")

def class_index(request, class_index):
    if returnAuthenticationStatus(request):
        selected_class = Class.objects.get(id=class_index)
        user_profile = retrieve_profile(request)
        if check_enrollment(selected_class, user_profile):
            create_assignment_url = "/main/create/" + str(class_index) 
            assignment_list = []
            assignments = selected_class.assignment_set.all().values("assignment_name", "id")
            print assignments
            for element in assignments:
                print element
                context_object = {}
                context_object["url"] = str(element["id"]) + "/"
                context_object["name"] = element["assignment_name"]
                assignment_list.append(context_object)
            return render(request, "main/class_index.html", {"assignment_list": assignment_list, "create_assignment_url": create_assignment_url})
        else:
            return HttpResponse("You do not have access to the class")
    else:
        return HttpResponse("Please log in")

def create_assignment(request, class_index):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            selected_class = Class.objects.get(id=class_index)
            user_profile = retrieve_profile(request)
            if check_access(selected_class, "TR", user_profile):
                Assignment.objects.create(assignment_name=request.POST["assignment_name"], class_id=selected_class)
                return HttpResponse("Done")
        else:
            form = AssignmentForm()
            return render(request, "main/create_assignment.html", {"form": form, "class_index" : class_index})
    else:
        return HttpResponse("You need to login")


        
def returnSubmission(user, assignment, selected_class):
    if len(assignment.textsubmission_set.all()) == 1:
        return assignment.textsubmission_set.all()[0]
    elif len(assignment.upload_set.all()) == 1:
        return assignment.upload_set.all()[0]
    else:
        return None

def view_assignment(request, class_index, assignment_index):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            selected_class = Class.objects.get(id=class_index)
            user_profile = retrieve_profile(request)
            if check_access(selected_class, "TR", user_profile):
                selected_assignment = Assignment.objects.get(id=assignment_index)
                if request.FILES:
                    Upload.objects.create(user=user_profile, assignment=selected_assignment, upload=request.FILES["myfile"])
                else:
                    TextSubmission.objects.create(user=user_profile, assignment=selected_assignment, text=request.POST["text"])
                return HttpResponse("Done")
            return HttpResponse("Authorization failed")
        else:
            user_profile = retrieve_profile(request)
            selected_class = Class.objects.get(id=class_index)
            if check_enrollment(selected_class, user_profile):
                selected_assignment = selected_class.assignment_set.get(id=assignment_index)
                submission = returnSubmission(user_profile, selected_assignment, selected_class)
                return render(request, "main/view_assignment.html", {"selected_assignment": selected_assignment, "submission" : submission})
            else:
                return HttpResponse("Denied")
    else:
        return HttpResponse("You have to sign in")

def main(request):
    return HttpResponse("This is the main page")
    
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
    
    