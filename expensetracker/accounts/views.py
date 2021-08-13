from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView


class RegistrationUserView(CreateView):
    pass


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('expenses:transactions')


class LogoutUserView(LoginRequiredMixin, LogoutView):
    pass
