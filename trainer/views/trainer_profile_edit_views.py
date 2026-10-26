from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import AccountType
from trainer.models import TrainerInfo
from trainer.forms import TrainerInfoForm

class TrainerOnlyMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.account_type != AccountType.TRAINER:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class TrainerInfoCreateView(TrainerOnlyMixin, CreateView):
    model = TrainerInfo
    form_class = TrainerInfoForm
    template_name = "trainer/profile/trainer_profile_edit.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "trainer_profile"):
            return redirect("trainer_profile")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("trainer_home")

class TrainerProfileEditView(TrainerOnlyMixin, UpdateView):
    model = TrainerInfo
    form_class = TrainerInfoForm
    template_name = "trainer/profile/trainer_profile_edit.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "trainer_profile"):
            return redirect("trainer_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return self.request.user.trainer_profile

    def get_success_url(self):
        return reverse("trainer_profile")