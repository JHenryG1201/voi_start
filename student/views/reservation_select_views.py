from django.utils import timezone
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from trainer.models import TrainerInfo, Lesson

class ReservationSelectView(LoginRequiredMixin, DetailView):
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        lesson_id = request.POST.get("lesson_id", "")
        lesson_type = request.POST.get("lesson_type")

        if lesson_type not in ("online", "offline") or not lesson_id.isdigit():
            return redirect(request.path)

        lesson = Lesson.objects.filter(
            pk=lesson_id,
            trainer=self.object.user,
            lesson_status="available",
            lesson_type__in=[lesson_type, "both"],
            lesson_date__gte=timezone.localdate(),
        ).first()
        if lesson is None:
            messages.error(request, "選択した日時は予約できません。")
            return redirect(request.path)

        request.session["reservation"] = {"lesson_id": lesson.pk, "lesson_type": lesson_type}
        return redirect("reservation_payment")