from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from trainer.forms import LessonReviewCreateForm
from trainer.models import Lesson, LessonReview

def session_key(pk):
    return f"review_data_{pk}"

class LessonMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.lesson = get_object_or_404(
                Lesson,
                pk=kwargs["pk"],
                student=request.user,
                lesson_status="done",
            )
            if (
                LessonReview.objects.filter(lesson=self.lesson).exists()
                and request.resolver_match.url_name != "lesson_review_done"
            ):
                return redirect("lesson_review_done", pk=self.lesson.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson"] = self.lesson
        context["trainer"] = self.lesson.trainer
        return context

class LessonReviewView(LessonMixin, FormView):
    template_name = "student/history/lesson_review.html"
    form_class = LessonReviewCreateForm

    def get_initial(self):
        return self.request.session.get(session_key(self.kwargs["pk"]), {})

    def form_valid(self, form):
        self.request.session[session_key(self.kwargs["pk"])] = form.cleaned_data
        return redirect("lesson_review_confirm", pk=self.kwargs["pk"])