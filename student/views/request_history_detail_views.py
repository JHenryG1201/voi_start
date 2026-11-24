from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from student.models import Feedback
from trainer.models import FeedbackReview

class RequestHistoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "student/history/request_history_detail.html"
    model = Feedback
    context_object_name = "feedback"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not FeedbackReview.objects.filter(feedback = context["feedback"]).exists():
            context["reviewable"] = True
        return context