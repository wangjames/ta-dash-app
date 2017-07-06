from __future__ import unicode_literals

from django.db import models

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
