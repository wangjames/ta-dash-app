from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ta_dash.storage import OverwriteStorage
def user_directory_path(instance, filename):
    assignment = instance.assignment
    assigning_class = assignment.class_id.name
    return '{0}/{1}/{2}'.format(instance.user.name, assigning_class, instance.upload_name)


    
class UserProfile(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
class Class(models.Model):
    name = models.CharField(max_length=200)
    participant = models.ManyToManyField(UserProfile, through='Enrollment')
class Meeting(models.Model):
    address = models.CharField(max_length=200)
    associated_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    meeting_date = models.CharField(max_length=200)

class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    access_choices = (("TR", 'Teacher'),
        ("ST", "Student"))
    access = models.CharField(
        max_length=2,
        choices=access_choices,
        default="ST",
    )
class PendingEnrollment(models.Model):
    inviter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="inviter")
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="recipient")
    class_candidate = models.ForeignKey(Class, on_delete=models.CASCADE)
    access_choices = (("TR", 'Teacher'),
        ("ST", "Student"))
    access = models.CharField(
        max_length=2,
        choices=access_choices,
        default="ST")
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

            
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    submission_type = models.CharField(max_length=200)
    upload_name = models.CharField(max_length=200)
    
    class Meta:
        abstract = True
    
class Upload(Submission):
    upload = models.FileField(max_length=255, storage=OverwriteStorage(), upload_to=user_directory_path)
    
class S3_Upload(models.Model):
    associated_submission = models.ForeignKey(Upload, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
class TextSubmission(Submission):
    text = models.CharField(max_length=200)

class AccountProfileID(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    profileID = models.IntegerField(unique=True)
    
class GoogleUser(models.Model):
    google_id = models.IntegerField(unique=True)
    userID = models.IntegerField(unique=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(name=instance.username, email=instance.email)
        AccountProfileID.objects.create(userID=instance, profileID=profile.id)

@receiver(pre_save, sender=Upload)
def delete_duplicate(sender, instance, **kwargs):
    try:
        this = Upload.objects.get(user=instance.user, assignment=instance.assignment)
        if this != None:
            this.delete()
    except:
        pass
@receiver(pre_save, sender= Meeting)
def delete_duplicate_meeting(sender, instance, **kwargs):
    try:
        this = Meeting.objects.get(associated_class=instance.associated_class)
        if this != None:
            this.delete()
    except:
        pass
    