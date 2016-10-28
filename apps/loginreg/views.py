from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import re

# Create your views here.

def index(request):
    return render(request, "loginreg/index.html")


def register(request):
    result = User.objects.validate(request.POST)
    if result[0] == False:
        for message in result[1]:
            messages.add_message(request, messages.INFO, message)
        return redirect('/')
    else:
        return createSession(request, result[1])

def login(request):
    result = User.objects.login(request.POST)
    if result[0] == False:
        messages.add_message(request, messages.INFO, result[1])
        return redirect('/')
    else:
        return createSession(request, result[1])

def logout(request):
    request.session.pop('user')
    return redirect('/')


def createSession(request, user):
    request.session['user'] = {
    "id": user.id,
    "name": user.name,
    "username": user.username
    }
    return redirect("wishlist:index")
