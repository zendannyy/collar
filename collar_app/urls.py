from django.contrib import admin
from django.urls import path
from . import views

app_name = 'collar'
urlpatterns = [
    path('', views.index),
	path('dash', views.dash),
	path('market', views.market),
	path('edit/<int:id>', views.edit),
    path('logout', views.logout),
	path('create', views.create),
	path('destroy', views.destroy),
]
