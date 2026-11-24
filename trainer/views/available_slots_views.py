from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q

from trainer.models import Lesson

class AvailableSlotsView(ListView):
    model = Lesson
    template_name = "trainer/reservation/available_slots.html"
    context_object_name = "slots"
    paginate_by = 5
    ordering = ["lesson_date", "lesson_start_time"]

    def get_queryset(self):

        now = timezone.localtime()
        today = now.date()
        current_time = now.time()

        (
            Lesson.objects
            .filter(trainer=self.request.user, lesson_status="available")
            .filter(
                Q(lesson_date__lt=today) |
                Q(lesson_date=today, lesson_start_time__lte=current_time)
            )
            .delete()
        )

        return Lesson.objects.filter(
            trainer=self.request.user,
            lesson_status="available",
        ).order_by("lesson_date", "lesson_start_time")