from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from trainer.models import Lesson

class ReservationListView(ListView, LoginRequiredMixin):
    template_name = "trainer/reservation/reservation_list.html"
    context_object_name = "lessons"
    model = Lesson
    paginate_by = 10
    ordering = ["lesson_date", "lesson_start_time"]

    def get_queryset(self):
        return (
            Lesson.objects
            .filter(trainer=self.request.user, lesson_status="reserved")
            .order_by("-lesson_date", "-lesson_start_time")
        )