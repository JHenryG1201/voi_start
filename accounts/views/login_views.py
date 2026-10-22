from django.contrib.auth.views import LoginView
from django.urls import reverse

from accounts.forms import AccountAuthenticationForm
from accounts.models import AccountType

class AccountLoginView(LoginView):
    form_class = AccountAuthenticationForm
    template_name = 'common/login.html'

    def get_success_url(self):
        if self.request.user.account_type == AccountType.TRAINER:
            return reverse('trainer_home')
        return reverse('student_home')