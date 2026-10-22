from django.views.generic import TemplateView

class AccountDeletionDoneView(TemplateView):
    template_name = 'common/account_delete_done.html'