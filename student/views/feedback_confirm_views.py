from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File
from django.db import transaction

from trainer.models import TrainerInfo
from student.models import Feedback

SESSION_KEY = "pending_feedback_request"
temp_storage = FileSystemStorage(location=settings.TEMP_UPLOAD_ROOT)

class FeedbackConfirmView(View, LoginRequiredMixin):
    template_name = "student/trainer_list/feedback/feedback_confirm.html"

    def get(self, request):
        pending = request.session.get(SESSION_KEY)
        if not pending:
            return redirect('feedback_upload')
        trainer = get_object_or_404(TrainerInfo, pk=pending["trainer_id"])
        return render(request, self.template_name, {"pending": pending, "trainer": trainer})
    
    def post(self, request):
        pending = request.session.get(SESSION_KEY)
        trianer = get_object_or_404(TrainerInfo, pk=pending["trainer_id"])
        if not pending:
            return redirect('feedback_upload')

        with transaction.atomic():
            feedback = Feedback(
                student = request.user,
                trainer = trianer.user,
                price = trianer.feedback_fee,
            )
            with temp_storage.open(pending["audio_path"], "rb") as f:
                feedback.audio.save(pending["original_name"], File(f), save=False)
            feedback.save()
        
        request.session["trainer_pk"] = pending["trainer_id"]

        temp_storage.delete(pending["audio_path"])
        del request.session[SESSION_KEY]

        return redirect("feedback_done", pk=feedback.pk)