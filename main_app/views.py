from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home(request):
  return render(request, 'index.html')

def login(request):
  return render(request, 'login.html')

def user(request):
  return render(request, 'user.html')