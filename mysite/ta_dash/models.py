from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    name = models.CharField(max_length=200)

class Class(models.Model):
    name = models.CharField(max_length=200)
    participant = models.ManyToManyField(UserProfile, through='Enrollment')

class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200, unique=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class Upload(Submission):
    upload = models.FileField(upload_to='uploads/')

class TextSubmission(Submission):
    text = models.CharField(max_length=200)

class AccountProfileID(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    profileID = models.IntegerField(unique=True)
    
class GoogleUser(models.Model):
    google_id = models.IntegerField(unique=True)
    userID = models.IntegerField(unique=True)

