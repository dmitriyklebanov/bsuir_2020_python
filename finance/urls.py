from django.urls import path
from .views import BalanceCreateView, BalancesListView, BalanceDetailView, BalanceUpdateView, BalanceDeleteView

urlpatterns = [
    path('balances/', BalancesListView.as_view(), name='balances'),
    path('balance/create/', BalanceCreateView.as_view(), name='balance_create'),
    path('balance/<int:pk>/', BalanceDetailView.as_view(), name='balance_detail'),
    path('balance/<int:pk>/update/', BalanceUpdateView.as_view(), name='balance_update'),
    path('balance/<int:pk>/delete/', BalanceDeleteView.as_view(), name='balance_delete'),
]
