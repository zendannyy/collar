from django.contrib.messages.api import error
from django.db import models
from login_reg_app.models import User
import bcrypt
import re


class JobManager(models.Manager):
    def job_validator(self, post_data):
        errors = {}
        
        if len(post_data['job']) < 4:
            errors["job"] = "Job Name should contain at least 4 characters"
        if len(post_data['duration']) < 1:
            errors["duration"] = "Duration estimate must be provided!"
        return errors


class Job(models.Model):
    """related_name is from views create function"""
    name = models.TextField(default='none')
    duration = models.TextField(default='none')
    worker = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

