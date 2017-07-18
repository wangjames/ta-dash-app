from django.shortcuts import render, redirect
import requests
from ta_dash.models import UserProfile, Class, Enrollment, AccountProfileID, Assignment, TextSubmission, Upload, PendingEnrollment, Meeting, S3_Upload
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ta_dash.forms import ClassForm, AssignmentForm, UserCreationForm, PendingEnrollmentForm, MeetingForm
import json, boto3, os
import sys
from django.http import JsonResponse

Yelp_Information = {
    "client_id": "HbhLE7U93kYuGMRsogCd0A",
    "client_secret": "O9bOeq6reFyBreYGRhTRrj2JNVHJoRj9HpgKx7it7EtykTWDGebyLB4mKKndSEZU",
    "grant_type": "client_credentials"
}

def getAuthenticationToken():
    url = "https://api.yelp.com/oauth2/token"
    response = requests.post(url, params=Yelp_Information)
    data = json.loads(response.text)
    return data["access_token"]
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
        return redirect("/main/")
def create_class(request):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            created_class = Class.objects.create(name=request.POST["name"])
            user_profile = retrieve_profile(request)
            created_enrollment = Enrollment.objects.create(enrolled_class=created_class, user=user_profile, access="TR")
            return redirect("/main/index")
        else:
            form = ClassForm()
            return render(request, 'main/create.html', {"form": form})
    else:
        return redirect("/main/")

def class_index(request, class_index):
    if returnAuthenticationStatus(request):
        selected_class = Class.objects.get(id=class_index)
        user_profile = retrieve_profile(request)
        if check_enrollment(selected_class, user_profile):
            create_assignment_url = "/main/create/" + str(class_index)
            create_meeting_url = "/main/class/" + str(class_index) + "/create_meeting/"
            assignment_list = []
            assignments = selected_class.assignment_set.all().values("assignment_name", "id")
            for element in assignments:
                context_object = {}
                context_object["url"] = str(element["id"]) + "/"
                context_object["name"] = element["assignment_name"]
                assignment_list.append(context_object)
            try:
                meeting = Meeting.objects.get(associated_class=selected_class)
            except: 
                meeting = {}
            return render(request, "main/class_index.html", {"assignment_list": assignment_list,
            "create_meeting_url": create_meeting_url,
            "create_assignment_url": create_assignment_url, "meeting": meeting, "class_index": class_index})
            
        else:
            return HttpResponse("You do not have access to the class")
    else:
        return redirect("/main/")
def return_suggestions(request):
    if request.method == "GET":
        address = request.GET.get("address","")
        category = request.GET.get("category","")
        param_dict = {"location": address, "categories": category}
        headers = {"Authorization": "Bearer " + getAuthenticationToken()}
        url = "https://api.yelp.com/v3/businesses/search"
        response = requests.get(url, params=param_dict, headers=headers)
        return HttpResponse(response)
    else:
        return redirect("/main/")
def create_meeting(request, class_index):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            selected_class = Class.objects.get(id=class_index)
            user_profile = retrieve_profile(request)
            if check_access(selected_class, "TR", user_profile):
                meeting_object = Meeting.objects.create(associated_class=selected_class, address=request.POST["address"], meeting_date=request.POST["meeting_date"])
                return redirect("/main/class/" + str(class_index))
            else:
                return HttpResponse("Not a teacher")
        else:
            form = MeetingForm()
            return render(request, 'main/find_meeting.html', {"form":form, "class_index": class_index})
def create_assignment(request, class_index):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            selected_class = Class.objects.get(id=class_index)
            user_profile = retrieve_profile(request)
            Assignment.objects.create(assignment_name=request.POST["assignment_name"], class_id=selected_class)
            return redirect("/main/class/" + class_index)
        else:
            form = AssignmentForm()
            return render(request, "main/create_assignment.html", {"form": form, "class_index" : class_index})
    else:
        return redirect("/main/")

def accept_invite(request, class_index):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            user_profile = retrieve_profile(request)
            selected_class = Class.objects.get(id=class_index)
            try:
                pending_enrollment = PendingEnrollment.objects.get(class_candidate=selected_class, recipient=user_profile)
                confirmed_enrollment = Enrollment.objects.create(enrolled_class=pending_enrollment.class_candidate, user=pending_enrollment.recipient)
                pending_enrollment.delete()
                return redirect("/main/index")
            except:
                return HttpResponse("No such invite")
        else:
            return HttpResponse("Must be posted")
    else:
        return redirect("/main/")
        
def get_invites(request):
    if returnAuthenticationStatus(request):
        user_profile = retrieve_profile(request)
        result_list = []
        try:
            invites = PendingEnrollment.objects.filter(recipient=user_profile).values('class_candidate')
            for element in invites:
                context_object = {}
                context_object["url"] =  "/main/invites/" + str(element["class_candidate"]) + "/"
                context_object["name"] = Class.objects.get(id=element["class_candidate"]).name
                result_list.append(context_object)
            return render(request, "main/invites.html", {"invite_list": result_list})
        except:
            return HttpResponse("No invites")
    else:
        return redirect("/main/")

def invite_user(request, class_index):
    if returnAuthenticationStatus(request):
        selected_class = Class.objects.get(id=class_index)
        user_profile = retrieve_profile(request)
        if check_enrollment(selected_class, user_profile):
            if request.method == "POST":
                recipient_email = request.POST["email"]
                try:
                    recipient = UserProfile.objects.get(email=recipient_email)
                    PendingEnrollment.objects.create(inviter=user_profile, recipient=recipient, class_candidate=selected_class)
                    return redirect("/main/index")
                except:
                    return HttpResponse("User does not exist")
            else:
                form = PendingEnrollmentForm()
                return render(request, "main/invite_class.html", {"form":form, "class_index": class_index})
        else:
            return HttpResponse("You are not in this class.")
    else:
        return redirect("/main/")
            
def returnSubmission(user, assignment, selected_class):
    if len(assignment.textsubmission_set.all()) == 1:
        return assignment.textsubmission_set.all()[0]
    elif len(assignment.upload_set.all()) == 1:
        return assignment.upload_set.all()[0]
    else:
        return None
def sign_s3(request):
    
    S3_BUCKET = "tadash-assets"

    file_name = request.GET.get('file_name', '')
    file_type = request.GET.get('file_type', '')
    
    s3client = boto3.client('s3')
    
    presigned_post = s3client.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
    )
    url_string = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    return HttpResponse(json.dumps({
    'data': presigned_post,
    'url': url_string
    }))
def guest_login(request):
    
    if not request.user.is_authenticated():
        user = authenticate(username="Guest", password="123qwe123")
        login(request, user)
        return redirect("/main/index")
    else:
        return redirect("/main/index")
def view_assignment(request, class_index, assignment_index):
    if returnAuthenticationStatus(request):
        if request.method == "POST":
            selected_class = Class.objects.get(id=class_index)
            user_profile = retrieve_profile(request)
            selected_assignment = Assignment.objects.get(id=assignment_index)
            if request.FILES:
                created_upload = Upload.objects.create(user=user_profile, assignment=selected_assignment, upload=request.FILES["file_input"], upload_name=str(request.FILES["file_input"]))
                s3_upload = S3_Upload.objects.create(associated_submission=created_upload, url=request.POST["upload-url"])
            else:
                TextSubmission.objects.create(user=user_profile, assignment=selected_assignment, text=request.POST["text"])
            return redirect("/main/class/" + class_index +"/")
        else:
            user_profile = retrieve_profile(request)
            selected_class = Class.objects.get(id=class_index)
            if check_enrollment(selected_class, user_profile):
                selected_assignment = selected_class.assignment_set.get(id=assignment_index)
                try:
                    selected_upload = Upload.objects.get(assignment=selected_assignment, user=user_profile)
                    s3_selected = S3_Upload.objects.get(associated_submission=selected_upload)
                    context_object = {}
                    context_object["url"] = s3_selected.url
                except:
                    context_object = {}
                return render(request, "main/view_assignment.html", {"selected_assignment": selected_assignment,
                "submission" : context_object,
                "class_index" : class_index,
                "assignment_index": assignment_index
                })
            else:
                return HttpResponse("Denied")
    else:
        return redirect("/main/")
def view_attendees(request, class_index):
    if returnAuthenticationStatus(request):
        selected_class = Class.objects.get(id=class_index)
        user_profile = retrieve_profile(request)
        result_list = []
        enrollments = Enrollment.objects.filter(enrolled_class=selected_class)
        for element in enrollments:
            context_object = {}
            context_object["url"] =  "/main/class/" + str(element.enrolled_class.id) + "/" + str(element.user.id) + "/view_class_user/"
            context_object["name"] = element.user.name
            result_list.append(context_object)
        return render(request, "main/view_students.html", {"user_list": result_list, "class_index": class_index})
    else:
        return redirect("/main/")
def view_submissions_by_user(request, user_index, class_index):
    if returnAuthenticationStatus(request):
        selected_class = Class.objects.get(id=class_index)
        user_profile = retrieve_profile(request)
        
        submission_list = []
        selected_user_profile = UserProfile.objects.get(id=user_index)
        assignments = Assignment.objects.filter(class_id=selected_class)

        for assignment in assignments:
            try:
                selected_upload = Upload.objects.get(assignment=assignment, user=user_profile)
                s3_selected = S3_Upload.objects.get(associated_submission=selected_upload)
                context_object = {}
                context_object["url"] = s3_selected.url
                context_object["name"] = assignment.assignment_name
                submission_list.append(context_object)
            except:
                continue
        return render(request, "main/view_submission.html", {"submission_list": submission_list, "class_index": class_index})
    else:
        return redirect("/main/")

def main(request):
    return render(request, "main/main.html", {})

def register(request):
    if request.method == "POST":
        finished_form = UserCreationForm(request.POST)
        if finished_form.is_valid():
            finished_form.save()
            username = finished_form.cleaned_data.get('username')
            raw_password = finished_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        return redirect("/main/index")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html',{"form":form})
    
