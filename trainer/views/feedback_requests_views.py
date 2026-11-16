from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from student.models import Feedback

class FeedbackRequestsView(LoginRequiredMixin, ListView):
    template_name = "trainer/feedback/feedback_requests.html"
    model = Feedback
    context_object_name = "feedbacks"
    paginate_by = 10

    def get_queryset(self):
        return (
            Feedback.objects
            .filter(trainer = self.request.user, status = "pending")
            .order_by("created_at")
        )