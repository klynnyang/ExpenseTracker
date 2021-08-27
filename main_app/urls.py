from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('user/', views.user, name='user'),
    path('email/', views.send_email, name='email'),
    path('budget/', views.budget_index, name='budget'),
    path('charts/<int:month_id>', views.chart, name='chart'), 
    path('tables/<int:month_id>', views.table, name='table'),
    path('budget/<int:budget_id>/', views.budget_detail, name='detail'),
    path('budget/<int:budget_id>/table_detail', views.table_detail, name='table_detail'),
    path('budget/<int:budget_id>/create', views.PurchaseCreate.as_view(), name='purchase_create'),
    path('purchase/<int:pk>/delete', views.PurchaseDelete.as_view(), name='purchase_delete'),
    path('purchase/<int:pk>/update', views.PurchaseUpdate.as_view(), name='purchase_update'),
]