from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404

from student.forms import FeedbackRequestForm
from trainer.models import TrainerInfo

SESSION_KEY = "pending_feedback_request"
temp_storage = FileSystemStorage(location=settings.TEMP_UPLOAD_ROOT)

class FeedbackUploadView(LoginRequiredMixin, FormView):
    form_class = FeedbackRequestForm
    template_name = "student/trainer_list/feedback/feedback_upload.html"
    success_url = reverse_lazy("feedback_payment")

    def dispatch(self, request, *args, **kwargs):
        self.trainer = get_object_or_404(TrainerInfo, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trainer"] = self.trainer
        return context

    def form_valid(self, form):
        session = self.request.session

        old = session.get(SESSION_KEY)
        if old:
            temp_storage.delete(old["audio_path"])

        audio = form.cleaned_data["audio"]
        saved_path = temp_storage.save(f"{self.request.user.pk}/{audio.name}", audio)

        session[SESSION_KEY] = {
            "audio_path": saved_path,
            "original_name": audio.name,
            # "content": form.cleaned_data["content"],
            "trainer_id": self.trainer.pk,
        }

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)