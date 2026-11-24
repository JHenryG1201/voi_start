from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q

from trainer.models import Lesson

class ReservationListView(ListView, LoginRequiredMixin):
    template_name = "trainer/reservation/reservation_list.html"
    context_object_name = "lessons"
    model = Lesson
    paginate_by = 10
    ordering = ["lesson_date", "lesson_start_time"]

    def get_queryset(self):

        now = timezone.localtime()
        today = now.date()
        current_time = now.time()

        (
            Lesson.objects
            .filter(trainer=self.request.user, lesson_status="reserved")
            .filter(
                Q(lesson_date__lt=today) |
                Q(lesson_date=today, lesson_end_time__lte=current_time)
            )
            .update(lesson_status="done")
        )
        
        return (
            Lesson.objects
            .filter(trainer=self.request.user, lesson_status="reserved")
            .order_by("-lesson_date", "-lesson_start_time")
        )