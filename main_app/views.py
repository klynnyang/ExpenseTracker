from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.urls.base import reverse_lazy
from .forms import EmailForm, MonthForm, SignUpForm
from django.http import JsonResponse
from .models import *
from django.db.models import Count, Sum, F
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth_login(request, user)
      return redirect('budget')
    else:
      error_message = form.errors
  form = SignUpForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def chart(request, month_id):
  labels = []
  data = []
  queryset = Purchase.objects.filter(date__month=month_id).order_by('date')
  for entry in queryset:
    labels.append(entry.date)
    data.append(entry.amount)
         
  return JsonResponse (data={
    'labels': labels,
    'data': data
  })

@login_required
def table(request, month_id):
  queryset = Purchase.objects.filter(date__month=month_id)
  total = queryset.values('category__name').annotate(total=Sum('amount'))
  total_list = list(total)
  return JsonResponse({'data': total_list})

class BudgetCreate(LoginRequiredMixin, CreateView):
  model = Budget
  fields = ['name']
  success_url = '/budget/'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PurchaseCreate(LoginRequiredMixin, CreateView):
  model = Purchase
  fields = '__all__'

class PurchaseDelete(LoginRequiredMixin, DeleteView):
  model = Purchase
  def get_success_url(self):
    return reverse_lazy('table_detail', kwargs={'budget_id': self.object.budget.id})

class PurchaseUpdate(LoginRequiredMixin, UpdateView):
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

@login_required
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

@login_required
def budget_index(request):
  budgets = Budget.objects.filter(user=request.user)
  return render(request, 'budget/index.html', {'budgets': budgets})

@login_required
def budget_detail(request, budget_id):
  budget = Budget.objects.get(id=budget_id)
  month = MonthForm()
  test=8
  return render(request, 'budget/detail.html', {'budget': budget, 'month': month, 'test':test})

@login_required
def table_detail(request, budget_id):
  budget = Budget.objects.get(id=budget_id)
  return render(request, 'budget/table_detail.html', {'budget': budget})

