from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from trainer.models import LessonReview

class LessonReviewDetailView(LoginRequiredMixin, DetailView):
    model = LessonReview
    context_object_name = "review"
    template_name = "student/history/lesson_review_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            LessonReview,
            lesson_id=self.kwargs["pk"],
            lesson__student=self.request.user,
        )
    