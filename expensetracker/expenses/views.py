from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Budget, Category, Transaction
from .forms import TransactionCreateForm, UpdateTransactionForm
from accounts.models import User
from .services import get_user_trans_data, statistics_img


class TransactionListView(ListView):
    template_name = 'expenses/transactions.html'
    context_object_name = 'transaction_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_amount'] = self.total_amount
        # if self.budget:
        #     context['budget'] = self.budget
        return context

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.request.user.pk)
        queryset = Transaction.objects.filter(user=self.user).order_by('-date')
        self.total_amount = get_user_trans_data(self.user, total_amount=True )
        self.budget = Budget.objects.filter(
            user=self.user).order_by('-date').first()
        return queryset


class CreateTransactionView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'expenses/transaction_create.html'
    form_class = TransactionCreateForm
    success_url = reverse_lazy('expenses:transactions')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UpdateTransactionView(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = 'expenses/transaction_update.html'
    form_class = UpdateTransactionForm
    success_url = reverse_lazy('expenses:transactions')

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(Transaction, pk=self.kwargs['transaction_pk'])


class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('expenses:transactions')

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(Transaction, pk=self.kwargs['transaction_pk'])

    # No confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CategoriesListView(ListView):
    template_name = 'expenses/categories.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['by_category'] = self.by_category

        # if self.budget:
        #     context['budget'] = self.budget
        return context

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.request.user.pk)
        queryset = Category.objects.all()
        self.by_category = get_user_trans_data(self.user, categories_amount=True)

        return queryset


class StatisticsView(TemplateView):
    template_name = 'expenses/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.request.user.pk)
        context['graphic_1'] = statistics_img(user,months_amount=True)
        context['graphic_2'] = statistics_img(user,categories_amount=True)
        context['graphic_3'] = statistics_img(user,total_income=True)
        return context