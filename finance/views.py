from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from finance.models import Balance


class BalancesListView(LoginRequiredMixin, ListView):
    model = Balance

    def get_queryset(self):
        return self.model.objects.filter(account=self.request.user)


class BalanceCreateView(LoginRequiredMixin, CreateView):
    model = Balance
    fields = ['name', 'amount', 'currency']

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)


class BalanceDetailView(LoginRequiredMixin, DetailView):
    model = Balance

    def get_object(self):
        obj = super(BalanceDetailView, self).get_object()
        if obj.account != self.request.user:
            raise PermissionDenied
        return obj


class BalanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Balance
    fields = ['name', 'amount']

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().account == self.request.user


class BalanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Balance
    success_url = reverse_lazy('balances')

    def test_func(self):
        return self.get_object().account == self.request.user
