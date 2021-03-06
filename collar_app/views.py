from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Category, Job, UserMessage, Comment
from login_reg_app.models import User
import bcrypt


def index(request):
	return redirect('/dash')

def market(request):
	"""market any logged in user sees"""
	try: #check if customer is logged in. This is in a try/except clause because if the user is not logged in the app will crash. The except clause will bring the user back to the login page.
		context = {
			"logged_user": User.objects.get(id=request.session['user_id']),
			"jobs": Job.objects.all(),
			"categories": Category.objects.all(),
			}
		return render(request, 'marketplace.html', context)
	except:
		return redirect('/signin/login')

def marketCategory(request, categoryID):
	"""market catgegory that was clicked"""
	try: #check if customer is logged in.
		context = {
			"logged_user": User.objects.get(id=request.session['userid']),
			"jobs": Job.objects.filter(category=Category.objects.get(id=categoryID)),
			}
		return render(request, 'marketplaceCategory.html', context)
	except:
		return redirect('/signin/login')

def marketSearch(request):
	"""market search from search form in navbar"""
	if request.method == 'POST':
		try: #check if customer is logged in. 
			context = {
				"logged_user": User.objects.get(id=request.session['userid']),
				"jobs": Job.objects.filter(name__icontains=request.POST['searchMarket']),
				}
			return render(request, 'marketplaceSearch.html', context)
		except:
			return redirect('/signin/login')
	return redirect('/')

# AJAX
def marketSearchAjax(request):
	"""ajax market search from search form in navbar"""
	if request.method == 'POST':
		try: #check if customer is logged in. 
			context = {
				"logged_user": User.objects.get(id=request.session['userid']),
				"jobs": Job.objects.filter(name__icontains=request.POST['searchMarket']),
				}
			return render(request, 'partials/market_table.html', context)
		except:
			return redirect('/signin/login')
	return redirect('/')

def dash(request):
	"""dashboard: only logged in worker user sees
	marketplace: logged in customer user sees. 
	This is in a try/except clause because if the user is not logged in the app will crash. The except clause will bring the user back to the login page."""
	try: 
		context = {
			"logged_user": User.objects.get(id=request.session['userid']),
			"jobs": Job.objects.all()
			}
		if request.session['isworker']: # this page only for worker users
			return render(request, 'dashboard.html', context)
		else:
			return redirect('/market')
	except:
		return redirect('/signin/login')

def create(request):
	"""workers can view jobs
	brings in related_name """
	try: # check if user logged in
		context = {
			'logged_user': User.objects.get(id=request.session['userid']), # if user is not logged in then this will jump to except clause
			'users': User.objects.all(),
			'jobs': Job.objects.all(),
		}
		if request.session['isworker']: # this page only for worker users
			return render(request, 'create.html', context)
		else:
			return render(request, 'marketplace.html', context)
	except:
		return redirect('/signin/login') # send to login page if not loggedin
	

def account(request):
	"""account profile from form in navbar"""
	try: #check if customer is logged in. 
		context = {
			"logged_user": User.objects.get(id=request.session['userid']),
			"jobs": Job.objects.all(),
			}
		return render(request, 'account.html', context)
	except:
		return redirect('/signin/login')


def edit(request):
	try: # check if user logged in
		context = {
			'logged_user': User.objects.get(id=request.session['userid']), # if user is not logged in then this will jump to except clause
			'users': User.objects.all(),
			'jobs': Job.objects.all(),
		}
		if request.session['isworker']: # this page only for worker users
			return render(request, 'edit.html', context)
		else:
			return render(request, 'marketplace.html', context)
	except:
		return redirect('/signin/login') # send to login page if not loggedin

def create_message(request):
	"""users can post a message and 'create' """
	# if 'email' not in request.session:
	# 	return redirect('/')
	# first_name key here
	context = {
		# 'first_name': request.session['first_name'],
		'user_messages': UserMessage.objects.all(),
		'comments': UserMessage.objects.all(),
	}
	return render(request, 'message.html', context)


def jobs(request):
	"""post message
	dash > post message"""
	print("creating message...")
	if request.method == 'POST':
		new_msg = UserMessage.objects.create(
			msg=request.POST['msg'],
			user=User.objects.get(id=request.session['userid'])		# changing to user_id 
		)
		new_msg.save()
	return redirect('/create_message')


def comment(request):
	"""post comments"""
	if request.method == 'POST':
		new_comment = Comment.objects.create(
			comment_text=request.POST['comment'],
			user=User.objects.get(id=request.session['userid']),			# changed this from user to user_id, changes to userid to match above method 
			message=UserMessage.objects.get(id=request.POST['message_id'])		# changed this from message to message_id
			# message=Message.objects.get(id=message_id)
		)
		new_comment.save()

	return redirect('create_message')


# redirects to login_reg_app to logout:
def logout(request):
	"""logout session, back to home page"""
	request.session.flush()
	return redirect('/signin/logout')



def destroy(request):
	"""destroy session with clear method"""
	request.session.clear()
	return redirect('/')

