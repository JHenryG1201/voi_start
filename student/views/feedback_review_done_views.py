from django.views.generic import TemplateView

from .feedback_review_views import FeedbackMixin

class FeedbackReviewDoneView(FeedbackMixin, TemplateView):
    template_name = "student/history/feedback_review_done.html"