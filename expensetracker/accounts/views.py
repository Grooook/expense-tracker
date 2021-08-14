from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView

from .forms import RegistrationUserForm
from .models import User

class RegistrationUserView(CreateView):
    model = User
    template_name = 'accounts/registration.html'
    form_class = RegistrationUserForm
    success_url = reverse_lazy('accounts:login')

class DeleteUserView(LoginRequiredMixin ,DeleteView):
    model = User
    success_url = reverse_lazy('accounts:registration')

    def get_object(self, queryset= None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(User, pk=self.request.user.pk)

    # No template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('expenses:transactions')


class LogoutUserView(LoginRequiredMixin, LogoutView):
    pass
