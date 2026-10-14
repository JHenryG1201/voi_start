from django.views.generic import TemplateView, CreateView
from .forms import AccountCreationForm
from django.urls import reverse_lazy

# Create your views here.
class RegisterView(CreateView):
    form_class = AccountCreationForm
    template_name = 'common/register.html'
    success_url = reverse_lazy('register_success')
    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)
    
class RegisterSuccessView(TemplateView):
    template_name = 'common/register_success.html'
