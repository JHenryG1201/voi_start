from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from trainer.models import FeedbackReview

class FeedbackReviewDetailView(LoginRequiredMixin, DetailView):
    model = FeedbackReview
    context_object_name = "review"
    template_name = "student/history/feedback_review_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            FeedbackReview,
            feedback_id=self.kwargs["pk"],
            feedback__student=self.request.user,
        )
    