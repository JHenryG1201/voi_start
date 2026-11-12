from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from student.models import Feedback

class FeedbackDoneView(LoginRequiredMixin, DetailView):
    template_name = "student/trainer_list/feedback/feedback_done.html"
    context_object_name = "feedback"
    model = Feedback