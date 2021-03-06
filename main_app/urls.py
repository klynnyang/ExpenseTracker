from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('user/', views.user, name='user'),
    path('email/', views.send_email, name='email'),
    path('budget/', views.budget_index, name='budget'),
    path('budget/create', views.budget_create, name='budget_create'),
    path('budget/share/<str:shared_url>/', views.add_budget, name='add_user_to_budget'),
    path('budget/<int:budget_id>/charts/<int:month_id>', views.chart, name='chart'), 
    path('budget/<int:budget_id>/tables/<int:month_id>', views.table, name='table'),
    path('budget/<int:budget_id>/', views.budget_detail, name='detail'),
    path('budget/<int:budget_id>/table_detail', views.table_detail, name='table_detail'),
    path('budget/<int:budget_id>/table_detail/<int:month_id>', views.table_detail_month, name='table_detail_month'),
    path('budget/<int:budget_id>/create', views.PurchaseCreate.as_view(), name='purchase_create'),
    path('purchase/<int:pk>/delete', views.PurchaseDelete.as_view(), name='purchase_delete'),
    path('purchase/<int:pk>/update', views.PurchaseUpdate.as_view(), name='purchase_update'),
    path('budget/share_link/<str:shared_url>', views.share_budget, name='share_budget'),
]