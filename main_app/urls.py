from django.core.mail import send_mail
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('user/', views.user, name='user'),
    path('email/', views.send_email, name='email'),
    path('budget/', views.budget_index, name='budget'),
]