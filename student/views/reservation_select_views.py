from django.utils import timezone
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from trainer.models import TrainerInfo, Lesson

class ReservationSelectView(DetailView):
    model = TrainerInfo
    template_name = "student/trainer_list/reservation/reservation_select.html"
    context_object_name = "trainer"

    def get_queryset(self):
        return TrainerInfo.objects.select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slots = Lesson.objects.filter(
            trainer=self.object.user, lesson_status="available",
            lesson_date__gte=timezone.localdate(),
        ).order_by("lesson_date", "lesson_start_time")

        context["slots"] = slots
        context["slot_data"] = [
            {
                "id": s.pk,
                "lesson_date": s.lesson_date.isoformat(),
                "lesson_start_time": s.lesson_start_time.strftime("%H:%M:%S"),
                "lesson_end_time": s.lesson_end_time.strftime("%H:%M:%S"),
                "lesson_type": s.lesson_type,
            }
            for s in slots
        ]
        return context