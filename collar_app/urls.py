from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
	path('dash', views.dash),
	# path('job/<int:id>', views.jobs),
    	path('logout', views.logout),
	path('create', views.create),
	path('destroy', views.destroy),
]
