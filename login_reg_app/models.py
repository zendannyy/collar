from django.db import models
# from datetime import datetime, timedelta
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # run all the functions and sum all the errors into one dictionary
        # The keys in 'errors' need to be empty if no errors

        f = self.reg_first_name(postData)
        if len(f) > 0:
            errors["first_name"] = f
        l = self.reg_last_name(postData)
        if len(l) > 0:
            errors["last_name"] = l
        e = self.reg_email(postData)
        if len(e) > 0:
            errors["email"] = e
        p = self.reg_password(postData)
        if len(p) > 0:
            errors["password"] = p
        c = self.reg_confirm_PW(postData)
        if len(c) > 0:
            errors["confirm_PW"] = c
        return errors

    # these are broken out seperately for ajax calls:
    # def reg_user_name(self, postData):
    #     error = ''
    #     if len(postData['user_name']) < 3:
    #         error = "Username should be at least 3 characters"
    #     if not postData['user_name'].isalpha():
    #         error = "Username should only be alphabetical characters"
    #     return error
    
    def reg_first_name(self, postData):
        error = ''
        if len(postData['first_name']) < 2:
            error = "First Name should be at least 2 characters"
        return error

    def reg_last_name(self, postData):
        error = ''
        if len(postData['last_name']) < 2:
            error = "Last Name should be at least 2 characters"
        return error

    def reg_email(self, postData):
        error = ''
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            error = ("Invalid email address.")
        if len(User.objects.filter(email=postData['email'].lower())) > 0: # works even if email is upper/lower case
            error = "Email already taken, email should be unique"
        return error

    def reg_password(self, postData):
        error = ''
        if len(postData['password']) < 10:
            more = 10-len(postData['password'])
            error = f"Weak Password! Password should be {more} more characters."
        return error

    def reg_confirm_PW(self, postData):
        error = ''
        if postData['confirm_PW'] != postData['password']:
            error = "Passwords need to match."
        return error



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    # user_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
	# max_length to 255, since it could get cut off and therefore not compare the same hash
    password = models.CharField(max_length=255)

    isWorker = models.BooleanField(default=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        isW = ''
        if self.isWorker:
            isW = 'Worker'
        else:
            isW = 'Customer'

        return f"{self.id}-{isW}:  {self.first_name}, {self.last_name}"
