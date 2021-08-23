from django.contrib.messages.api import error
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def reg_validator(self, post_data):
        """validator for reg
        all keys come from form in index.html"""
        errors = {}
      
        if len(post_data['user_name']) < 3:
            errors["user_name"] = "Username should be at least 3 characters"
        if not post_data['user_name'].isalpha():
            errors["user_name"] = "Username should only be alphabetical characters"
            
        email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not email_re.match(post_data['email']):
            errors['email'] = "Invalid email address"

		# even if empty, filter won't break
        users_with_email = User.objects.filter(
			email=post_data['email'])
        if len(users_with_email) >= 1:
            errors['dupe'] = "Email is registered, choose another"

        if len(post_data['password']) < 10:
            errors['password'] = "Password is too short, 12 or more characters please"
        elif post_data['password'] != post_data['confirm_pw']:
            errors['match'] = "Password does not match password confirmation"

        return errors
    
 

    def login_validator(self, post_data, request):
        """validator for username nas pw
        request is for passing in session"""
        errors = {}
        if len(post_data['user_name']) < 3:
            errors["user_name"] = "Username should be at least 3 characters"
        if not post_data['user_name'].isalpha():
            errors["user_name"] = "Username should only be alphabetical characters"
            request.session['user_name'] = ""
        else:
            login_user = post_data['user_name'].lower()
            user = User.objects.filter(user_name=login_user)
            if user:
                logged_user = user[0]
                print(logged_user)
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id
                else:
                    errors['pass'] = "Incorrect password, please try again."
            else:
                request.session['user_name'] = ""
                errors['user_name'] = "Username doesn't exist. Please register first."
        return errors


class User(models.Model):
	user_name = models.CharField(max_length=20)
	email = models.CharField(max_length=20)
	# max_length to 255, since it could get cut off and therefore not compare the same hash
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class JobManager(models.Manager):
    def job_validator(self, post_data):
        errors = {}
        
        if len(post_data['job']) < 4:
            errors["job"] = "Job Name should contain at least 4 characters"
        if len(post_data['duration']) < 1:
            errors["duration"] = "Duration estimate must be provided!"
        return errors


class Jobs(models.Model):
    """related_name is from views create function"""
    job = models.TextField(default='none')
    duration = models.TextField(default='none')
    worker = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

