from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404

from trainer.models import TrainerInfo

SESSION_KEY = "pending_feedback_request"
temp_storage = FileSystemStorage(location=settings.TEMP_UPLOAD_ROOT)

class FeedbackPaymentView(View, LoginRequiredMixin):
    template_name = "student/trainer_list/feedback/feedback_payment.html"

    def get(self, request):
        pending = request.session.get(SESSION_KEY)
        if not pending:
            return redirect('feedback_upload')
        trainer = get_object_or_404(TrainerInfo, pk=pending["trainer_id"])
        return render(request, self.template_name, {"pending": pending, "trainer": trainer})
    
    def post(self, request):
        pending = request.session.get(SESSION_KEY)
        if not pending:
            return redirect('feedback_upload')
        
        return redirect("feedback_confirm")