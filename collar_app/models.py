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

class Category(models.Model):
    name = models.CharField(max_length=45, default='none')
    description = models.TextField(default='none', null=True)
    # jobs = the jobs that are in this category

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Job(models.Model):
    """related_name is from views create function"""
    name = models.TextField(default='none')
    duration = models.TextField(default='none')
    worker = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='job_category', on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.worker.first_name}:  {self.name}"


class UserMessage(models.Model):
	msg = models.TextField()
	user = models.ForeignKey(User, related_name='messages',
							 on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



class Comment(models.Model):
	comment_text = models.TextField(default='comment_text')
	user = models.ForeignKey(User, related_name='comments', default=0, on_delete=models.CASCADE)
	message = models.ForeignKey(UserMessage, related_name='comments', default='message', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
