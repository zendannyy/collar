from django.contrib import admin
from django.urls import path
from . import views

app_name = 'collar'
urlpatterns = [
    path('', views.index),
	path('dash', views.dash),
	path('market', views.market),
	path('market/<int:categoryID>', views.marketCategory),
	path('market/search', views.marketSearch),
	path('market/search/ajax', views.marketSearchAjax),
	path('edit/<int:id>', views.edit),
    path('logout', views.logout),
	path('create', views.create),
	path('create_message', views.create_message),
	path('comment', views.comment),
	path('account', views.account),
	path('market/message', views.message),
	path('destroy', views.destroy),
]
