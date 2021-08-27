from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.urls.base import reverse_lazy
from .forms import EmailForm, MonthForm
from django.http import JsonResponse
from .models import *
from django.db.models import Count, Sum, F
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
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

def table(request, month_id):
  queryset = Purchase.objects.filter(date__month=month_id)
  total = queryset.values('category__name').annotate(total=Sum('amount'))
  total_list = list(total)
  return JsonResponse({'data': total_list})

class PurchaseCreate(CreateView):
  model = Purchase
  fields = '__all__'

class PurchaseDelete(DeleteView):
  model = Purchase
  def get_success_url(self):
    return reverse_lazy('table_detail', kwargs={'budget_id': self.object.budget.id})

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
  month = MonthForm()
  test=8
  return render(request, 'budget/detail.html', {'budget': budget, 'month': month, 'test':test})

def table_detail(request, budget_id):
  budget = Budget.objects.get(id=budget_id)
  return render(request, 'budget/table_detail.html', {'budget': budget})

