from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect

from student.models import Feedback

class FeedbackRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "trainer/feedback/feedback_request_detail.html"
    model = Feedback
    context_object_name = "feedback"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        added_feedback = request.POST.get("feedback")
        self.object.feedback = added_feedback
        self.object.feedback_time = timezone.now()
        self.object.status = "done"
        self.object.save(update_fields=["feedback", "feedback_time", "status"])
        return redirect("feedback_sent")