from django.views.generic import View
from django.shortcuts import redirect, render

from .feedback_review_views import FeedbackMixin, session_key
from trainer.forms import FeedbackReviewCreateForm

class FeedbackReviewConfirmView(FeedbackMixin, View):
    template_name = "student/history/feedback_review_confirm.html"

    def get(self, request, *args, **kwargs):
        data = request.session.get(session_key(kwargs["pk"]))
        rating = data["rating"]
        if not data:
            return redirect("feedback_review", pk=kwargs["pk"])
        return render(request, self.template_name, {
            "stars": [i <= rating for i in range(1, 6)],
            "feedback": self.feedback,
            "trainer": self.feedback.trainer,
            "data": data,
        })

    def post(self, request, *args, **kwargs):
        key = session_key(kwargs["pk"])
        data = request.session.get(key)
        if not data:
            return redirect("feedback_review", pk=kwargs["pk"])

        form = FeedbackReviewCreateForm(data)
        if not form.is_valid():
            return redirect("feedback_review", pk=kwargs["pk"])

        review = form.save(commit=False)
        review.feedback = self.feedback
        review.save()

        del request.session[key]
        return redirect("feedback_review_done", pk=kwargs["pk"])
