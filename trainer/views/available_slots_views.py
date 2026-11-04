from django.views.generic import ListView

from trainer.models import Lesson

class AvailableSlotsView(ListView):
    model = Lesson
    template_name = "trainer/reservation/available_slots.html"
    context_object_name = "slots"
    paginate_by = 5
    ordering = ["lesson_date", "lesson_start_time"]

    def get_queryset(self):
        return Lesson.objects.filter(
            trainer=self.request.user,
        ).order_by("lesson_date", "lesson_start_time")