from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
	path('register', views.register),
	path('dash', views.dash),
	# path('job/<int:id>', views.jobs),
	path('create', views.create),
	path('destroy', views.destroy),
	path('logout', views.logout),


]
