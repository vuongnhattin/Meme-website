from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from api.models import *
from api.serializers import *
from django.contrib.auth.models import User, Group
import requests
from django.http import *
from django.urls import reverse
import json
from rest_framework.authtoken.models import Token
from .forms import *
# Create your views here.

def isInGroup(user, group_name):
    return user.groups.filter(name=group_name).exists()

@login_required(login_url='app:login')
def home(request):
    return render(request, 'index.html')

def register_view(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
    
    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.GET.get('next')
        if not next:
            next = '/home/'
        print(next)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next)

    return render(request, 'login.html')

@login_required(login_url='app:login')
def logout_view(request):
    logout(request)
    return redirect('app:login')

@login_required(login_url='app:login')
def items_view(request):
    auth_token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'format': ''
    }

    query_string = request.META.get('QUERY_STRING', '')
    print(query_string)

    response = requests.get(f"http://127.0.0.1:8000{reverse('api:items')}?{query_string}", headers=headers)

    context = {'data': response.json(), 'user': request.user}
    template = 'items_manager.html' if isInGroup(request.user, 'Manager') else 'items.html'

    return render(request, template, context)

@login_required(login_url='app:login')
def cart_view(request):
    auth_token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(f"http://127.0.0.1:8000{reverse('api:cart')}", headers=headers)

    context = {'data': response.json(), 'user': request.user}

    return render(request, 'cart.html', context)

def upload_view(request):
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            temp_form = form.save(commit=False) # Not save to database yet

            if isInGroup(request.user, 'Manager'):
                temp_form.approved = True
            
            temp_form.save()
            return redirect('app:upload_success')

    return render(request, 'upload.html', {'form': form})

def upload_success_view(request):
    message = 'Upload successfully.' if isInGroup(request.user, 'Manager') else 'Send request successfully, please wait for the admin to verify your post.'

    return render(request, 'upload_success.html', {'message': message})
