from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from trainer.models import Lesson, LessonReview

class ReservationHistoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "student/history/reservation_history_detail.html"
    model = Lesson
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not LessonReview.objects.filter(lesson = context["lesson"]).exists():
            context["reviewable"] = True
        return context