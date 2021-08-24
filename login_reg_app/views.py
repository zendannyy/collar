from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from datetime import datetime
import bcrypt

# Login page
def login(request):
    """if a user is logged in prevent relogin from a different user because we do not want to overwrite the session data.
    User needs to log out first then they can go to login.html to login/register"""
    try: 
        if request.session['userid']:
            context = {"User": User.objects.get(id=request.session['userid'])}
            print(request.session['userid'])
            return redirect('/dash')
    except:
        return render(request, 'login.html')

# Register page
def register(request):
    """if a user is logged in prevent relogin from a different user because we do not want to overwrite the session data.
    User needs to log out first then they can go to login.html to login/register"""
    try: 
        if request.session['userid']:
            context = {"User": User.objects.get(id=request.session['userid'])}
            return redirect('/dash')
    except:
        return render(request, 'register.html')
#--------------------------------------------------------
# LOGIN/REGISTRATION
#--------------------------------------------------------
# POST
def registering(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/signin/register')
        else:
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'].lower(), #email not case sensitive
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['userid'] = User.objects.last().id
            return redirect('/dash')
    return redirect('/signin/register')

# POST
def logining(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'].lower()) #find user with email not case sensative
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/dash')
        else:
            messages.error(request, "Invalid credentials.", extra_tags='login')
            return redirect('/signin/login')
    return redirect('/signin/login')

# POST
def logout(request):
    del request.session['userid']
    return redirect('/signin/login')
    


# AJAX validations for registration page---------------------------------
def register_validations(request, code):
    if request.method == 'POST':
        bad = False
        divID = ''
        #code: 0 = first_name, 1 = last_name, 2 = email, 3 = password, 4 = confirm_PW,
        if code == 0:
            error = User.objects.reg_first_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
            divID = 'first_name'
        elif code == 1:
            error = User.objects.reg_last_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
            divID = 'last_name'
        elif code == 2:
            error = User.objects.reg_email(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Email available!'
            divID = 'email'
        elif code == 3:
            error = User.objects.reg_password(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Strong password!'
            divID = 'password'
        elif code == 4:
            error = User.objects.reg_confirm_PW(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Passwords match!'
            divID = 'confirm_PW'
        context = {
            'bad': bad,
            'error': error,
            'divID': divID
        }
        print(context['error'])
        return render(request, 'partials/reg_validate.html', context)  
    return redirect('/register')