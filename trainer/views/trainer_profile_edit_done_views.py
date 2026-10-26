from django.views.generic import TemplateView

from .trainer_profile_edit_views import TrainerOnlyMixin

class TrainerProfileEditDoneView(TrainerOnlyMixin, TemplateView):
    template_name = 'trainer/profile/trainer_profile_edit_done.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["is_create"] = self.request.GET.get("mode") == "create"
        return ctx