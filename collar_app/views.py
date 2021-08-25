from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Job
from login_reg_app.models import User
import bcrypt


def index(request):
	return redirect('/dash')




def dash(request):
	"""dashboard logged in user sees"""
	try: #check if customer is logged in. This is in a try/except clause because if the user is not logged in the app will crash. The except clause will bring the user back to the login page.
		context = {"logged_user": User.objects.get(id=request.session['userid'])}
		return render(request, 'dashboard.html', context)
	except:
		return redirect('/signin/login')


def create(request):
	"""workers can view jobs
	brings in related_name """
	try: # check ig user logged in
		context = {
			'logged_user': User.objects.get(id=request.session['user_id']), # if user is not logged in then this will jump to except clause
			'users': User.objects.all(),
			'jobs': Job.objects.all(),
		}
		return render(request, 'dashboard.html', context)
	except:
		return redirect('/signin/login') # send to login page if not loggedin
	

def logout(request):
	"""logout session, back to home page"""
	request.session.flush()
	print(request.session)
	return redirect('/')



def destroy(request):
	"""destroy session with clear method"""
	request.session.clear()
	return redirect('/')

