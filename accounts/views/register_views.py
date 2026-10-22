from django.views.generic import CreateView
from django.urls import reverse_lazy

from accounts.forms import AccountCreationForm

class RegisterView(CreateView):
    form_class = AccountCreationForm
    template_name = 'common/register.html'
    success_url = reverse_lazy('register_done')