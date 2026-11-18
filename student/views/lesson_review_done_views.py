from django.views.generic import TemplateView

from .lesson_review_views import LessonMixin

class LessonReviewDoneView(LessonMixin, TemplateView):
    template_name = "student/history/lesson_review_done.html"