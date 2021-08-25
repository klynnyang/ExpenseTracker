from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from .forms import EmailForm
from .models import *

# Create your views here.
def home(request):
  form = EmailForm()
  return render(request, 'index.html', {
    'form': form
  })

def login(request):
  return render(request, 'login.html')

def user(request):
  return render(request, 'user.html')

def send_email(request):
  messageSent = False
  if request.method == 'POST':
    form = EmailForm(request.POST)
    if form.is_valid():
      subject = 'You got an invite!'
      message = 'Hello'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [form.cleaned_data['recipient']]
      html_message = loader.render_to_string(
            'email.html',
            {
                'user_name': form.cleaned_data['recipient'],
                'subject':  'You got an invite from ___ to join Expense Tracker!',
            }
        )
      send_mail(subject, message, email_from, recipient_list, fail_silently=True, html_message=html_message)
      messageSent = True
  else:
    form = EmailForm()
  return render(request, 'index.html', {'form': form, 'messageSent':messageSent})

def budget_index(request):
  budget = Budget.objects.all()
  return render(request, 'budget/index.html', {'budget': budget})