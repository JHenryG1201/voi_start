from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import logout

from accounts.forms import AccountDeletionForm

class AccountDeletionView(LoginRequiredMixin, FormView):
    template_name = 'common/account_delete.html'
    form_class = AccountDeletionForm
    success_url = reverse_lazy('account_delete_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        account = self.request.user
        logout(self.request)
        account.delete()
        return super().form_valid(form)