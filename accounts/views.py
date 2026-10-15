from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import AccountAuthenticationForm, AccountCreationForm
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
