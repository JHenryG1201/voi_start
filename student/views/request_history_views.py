from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from student.models import Feedback

class RequestHistoryView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = "student/history/request_history.html"
    context_object_name = "feedbacks"

    def get_queryset(self):
        return (
            Feedback.objects
            .filter(student=self.request.user)
            .select_related("trainer")
            .order_by("created_at")
        )