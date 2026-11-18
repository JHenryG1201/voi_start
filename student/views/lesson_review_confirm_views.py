from django.views.generic import View
from django.shortcuts import redirect, render

from .lesson_review_views import LessonMixin, session_key
from trainer.forms import LessonReviewCreateForm

class LessonReviewConfirmView(LessonMixin, View):
    template_name = "student/history/lesson_review_confirm.html"

    def get(self, request, *args, **kwargs):
        data = request.session.get(session_key(kwargs["pk"]))
        rating = data["rating"]
        if not data:
            return redirect("lesson_review", pk=kwargs["pk"])
        return render(request, self.template_name, {
            "stars": [i <= rating for i in range(1, 6)],
            "lesson": self.lesson,
            "trainer": self.lesson.trainer,
            "data": data,
        })

    def post(self, request, *args, **kwargs):
        key = session_key(kwargs["pk"])
        data = request.session.get(key)
        if not data:
            return redirect("lesson_review", pk=kwargs["pk"])

        form = LessonReviewCreateForm(data)
        if not form.is_valid():
            return redirect("lesson_review", pk=kwargs["pk"])

        review = form.save(commit=False)
        review.lesson = self.lesson
        review.save()

        del request.session[key]
        return redirect("lesson_review_done", pk=kwargs["pk"])
