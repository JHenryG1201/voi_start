from django.views.generic import DetailView
from django.shortcuts import redirect

from .trainer_profile_edit_views import TrainerOnlyMixin
from trainer.models import TrainerInfo

class TrainerProfileView(TrainerOnlyMixin, DetailView):
    model = TrainerInfo
    template_name = "trainer/profile/trainer_profile.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "trainer_profile"):
            return redirect("trainer_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return self.request.user.trainer_profile