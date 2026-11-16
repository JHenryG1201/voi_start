from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from student.models import Feedback

class FeedbackRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "trainer/feedback/feedback_request_detail.html"
    model = Feedback
    context_object_name = "feedback"