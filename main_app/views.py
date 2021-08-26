from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.urls.base import reverse_lazy
from .forms import EmailForm
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

class PurchaseCreate(CreateView):
  model = Purchase
  fields = '__all__'

class PurchaseDelete(DeleteView):
  model = Purchase
  def get_success_url(self):
    return reverse_lazy('detail', kwargs={'budget_id': self.object.budget.id})

class PurchaseUpdate(UpdateView):
  model = Purchase
  fields = '__all__'

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
  budgets = Budget.objects.all()
  return render(request, 'budget/index.html', {'budgets': budgets})

def budget_detail(request, budget_id):
  budget = Budget.objects.get(id=budget_id)
  return render(request, 'budget/detail.html', {'budget': budget})

def table_detail(request, budget_id):
  budget = Budget.objects.get(id=budget_id)
  return render(request, 'budget/table_detail.html', {'budget': budget})

