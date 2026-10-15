from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import (
    AccountAuthenticationForm,
    AccountCreationForm,
    AccountDeletionForm,
)
from .models import AccountType

# Create your views here.
class RegisterView(CreateView):
    form_class = AccountCreationForm
    template_name = 'common/register.html'
    success_url = reverse_lazy('register_success')


class AccountLoginView(LoginView):
    form_class = AccountAuthenticationForm
    template_name = 'common/login.html'

    def get_success_url(self):
        if self.request.user.account_type == AccountType.TRAINER:
            return reverse('trainer_home')
        return reverse('student_home')


class RegisterSuccessView(TemplateView):
    template_name = 'common/register_success.html'


class AccountDeletionView(LoginRequiredMixin, FormView):
    template_name = 'common/account_delete.html'
    form_class = AccountDeletionForm
    success_url = reverse_lazy('account_delete_success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        account = self.request.user
        logout(self.request)
        account.delete()
        return super().form_valid(form)

class AccountDeletionSuccessView(TemplateView):
    template_name = 'common/account_delete_success.html'