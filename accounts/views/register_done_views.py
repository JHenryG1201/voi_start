from django.views.generic import TemplateView

class RegisterDoneView(TemplateView):
    template_name = 'common/register_done.html'