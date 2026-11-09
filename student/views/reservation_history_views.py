from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from trainer.models import Lesson

class ReservationHistoryView(LoginRequiredMixin, ListView):
    template_name = "student/history/reservation_history.html"
    model = Lesson
    context_object_name = "done"
    paginate_by = 10
    ordering = ["lesson_date", "lesson_start_time"]

    def get_queryset(self):
        return (
            Lesson.objects
            .filter(student=self.request.user, lesson_status="done")
            .select_related("trainer")
            .order_by("-lesson_date", "-lesson_start_time")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reserved"] = (
            Lesson.objects
            .filter(student=self.request.user, lesson_status="reserved")
            .select_related("trainer__trainer_profile")
            .order_by("-lesson_date", "-lesson_start_time")
        )
        return context