from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from trainer.forms import FeedbackReviewCreateForm
from trainer.models import FeedbackReview
from student.models import Feedback

def session_key(pk):
    return f"review_data_{pk}"

class FeedbackMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.feedback = get_object_or_404(
                Feedback,
                pk=kwargs["pk"],
                student=request.user,
                status="done",
            )
            if (
                FeedbackReview.objects.filter(feedback=self.feedback).exists()
                and request.resolver_match.url_name != "feedback_review_done"
            ):
                return redirect("feedback_review_done", pk=self.feedback.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback"] = self.feedback
        context["trainer"] = self.feedback.trainer
        return context

class FeedbackReviewView(FeedbackMixin, FormView):
    template_name = "student/history/feedback_review.html"
    form_class = FeedbackReviewCreateForm

    def get_initial(self):
        return self.request.session.get(session_key(self.kwargs["pk"]), {})

    def form_valid(self, form):
        self.request.session[session_key(self.kwargs["pk"])] = form.cleaned_data
        return redirect("feedback_review_confirm", pk=self.kwargs["pk"])