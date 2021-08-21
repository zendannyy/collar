from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
import bcrypt


def index(request):
	return render(request, 'index.html')
