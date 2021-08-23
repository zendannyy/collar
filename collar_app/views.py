from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
import bcrypt


def index(request):
	return render(request, 'index.html')

def login(request):
    # if a customer is logged in prevent relogin from a different customer because we do not want to overwrite the session data. Customer needs to log out first then they can go to login.html to login/register
    # try: 
    #     if request.session['user_id']:
    #         context = {"User": User.objects.get(id=request.session['user_id'])}
    #         print(request.session['user_id'])
    #         return redirect('/dash')
    # except:
    #     return render(request, 'login.html')
	# return redirect("/login")

	try:
		if request.method == 'GET':
			return render(request, "login.html")
	except ValueError:
		pass
	errors = User.objects.login_validator(request.POST, request)

	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/login')

	user = User.objects.filter(
		user_name=request.POST['user_name'])  # why are we using filter here instead of get

	if len(user) > 0:		# if this isn't triggered, inner else statement executes
		logged_user = user[0]
		# use bcrypt's check_pw method, passing the hash from db and the pw from the form
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
			# if we get True after checking the password, we have to put the user id in session
			request.session['user_id'] = logged_user.id
			return redirect('/dash')
		else:
			messages.error(request, 'Username or password did not match')
	# if the passwords don't match, redirect to stay in login
	return redirect("/login")


def register(request):
	errors = User.objects.reg_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		# Create User
		hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
		user = User.objects.create(
			user_name=request.POST['user_name'],
			email=request.POST['email'], password=hash_pw
			# password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt().decode())
		)
		request.session['user_id'] = user.id
		return redirect('/dash')



def dash(request):
	"""dashboard logged in user sees"""
	context = {
		"logged_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'dashboard.html', context)


def create(request):
	"""workers can view jobs
	brings in related_name """
	context = {
		'logged_user': User.objects.get(id=request.session['user_id']),
		'users': User.objects.all(),
		'jobs': Jobs.objects.all(),
	}
	return render(request, 'dashboard.html', context)



def destroy(request):
	"""destroy session with clear method"""
	request.session.clear()
	return redirect('/')

def logout(request):
	"""logout session, back to home"""
	request.session.flush()
	print(request.session)
	return redirect('/')
