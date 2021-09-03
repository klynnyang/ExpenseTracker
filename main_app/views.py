from .models import *
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from .forms import EmailForm, MonthForm, BudgetForm, PurchaseForm, SignUpForm
from django.http import JsonResponse
from django.db.models import Count, Sum, F
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from bootstrap_modal_forms.generic import BSModalCreateView

from django.contrib.auth.models import User

# Create your views here.

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('budget')
    else:
      error_message = form.errors
  form = SignUpForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'account/signup.html', context)

@login_required
def budget_create(request):
  if request.method == 'GET':
    form = BudgetForm()
    return render(request, 'main_app/budget_form.html', {
      'form': form
    })
  if request.method == 'POST':
    if not request.is_ajax():
      form = BudgetForm(request.POST)
      if form.is_valid():
        new_budget = form.save()
        new_budget.user.add(request.user.id)
        new_budget.save()
    return redirect('budget')

@login_required
def budget_submit(request):
  form = BudgetForm(request.POST)
  if form.is_valid():
    new_budget = form.save()
    new_budget.user.add(request.user.id)
    new_budget.save()
  return redirect('budget')

@login_required
def chart(request, budget_id, month_id):
  labels = []
  data = []
  queryset = Purchase.objects.filter(budget=budget_id).filter(date__month=month_id)
  new_query = list(queryset.values('date').annotate(total=Sum('amount')).order_by('date'))
  for entry in new_query:
    labels.append(entry["date"])
    data.append(entry["total"])
         
  return JsonResponse (data={
    'labels': labels,
    'data': data,
    'id': budget_id
  })

@login_required
def table(request, budget_id, month_id):
  labels = []
  chart_data = []
  queryset = Purchase.objects.filter(budget=budget_id).filter(date__month=month_id)
  total = list(queryset.values('category__name').annotate(total=Sum('amount')))
  for entry in total:
    labels.append(entry["category__name"])
    chart_data.append(entry["total"])
  return JsonResponse(data={
    'data': total, 
    'id': budget_id,
    'labels': labels,
    'chart': chart_data
  })

@login_required
def table_detail_month(request, budget_id, month_id):
  queryset = Purchase.objects.filter(budget=budget_id).filter(date__month=month_id)
  new_query = list(queryset.values(
    'id','amount','date', 'notes',
    username = F("user__username"),
    categoryname = F("category__name"),
    retailername = F("retailer__name"),
   ))
  return JsonResponse(data={
    'data': new_query,
  })

class PassRequestToFormView:
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request
    return kwargs

class PurchaseCreate(LoginRequiredMixin, PassRequestToFormView, CreateView):
  form_class = PurchaseForm
  model = Purchase

class PurchaseUpdate(LoginRequiredMixin, PassRequestToFormView, UpdateView):
  model = Purchase
  form_class = PurchaseForm

class PurchaseDelete(LoginRequiredMixin, DeleteView):
  template_name = "main_app/purchase_confirm_delete.html"
  model = Purchase
  def get_success_url(self):
    return reverse_lazy('table_detail', kwargs={'budget_id': self.object.budget.id})

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
      print(form.cleaned_data['share_url'])
      subject = 'You got an invite!'
      message = 'Hello'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [form.cleaned_data['recipient']]
      html_message = loader.render_to_string(
            'email.html',
            {
                'user_name': form.cleaned_data['recipient'],
                'url': form.cleaned_data['share_url'],
                'subject':  'You got an invitation to join Expense Tracker!',
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
def share_budget(request, shared_url):
  form = EmailForm()
  budget = Budget.objects.get(shared_url = shared_url)
  return render(request, 'main_app/share_budget.html', {'budget': budget, 'form': form})

@login_required
def add_budget(request, shared_url):
  Budget.objects.get(shared_url=shared_url).user.add(request.user.id)
  return redirect('/budget/')

@login_required
def budget_detail(request, budget_id):
  budget = Budget.objects.get(id=budget_id)
  if request.user not in budget.user.all():
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budget/index.html', {'budgets': budgets})
  else:
    month = MonthForm()
    not_shared_users = User.objects.exclude(id__in = budget.user.all().values_list('id'))
    test=datetime.now().month
    return render(request, 'budget/detail.html', { 'not_shared_users': not_shared_users, 'budget': budget, 'month': month, 'test':test})

@login_required
def table_detail(request, budget_id):
  month = MonthForm()
  test = datetime.now().month
  budget = Budget.objects.get(id=budget_id)
  return render(request, 'budget/table_detail.html', {'budget': budget, 'month':month, 'test':test})

