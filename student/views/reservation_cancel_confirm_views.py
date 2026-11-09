from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from trainer.models import Lesson, TrainerInfo


def get_cancellable_lesson(request, pk):
    return Lesson.objects.select_related("trainer").filter(
        pk=pk,
        student=request.user,
        lesson_status="reserved",
        lesson_date__gt=timezone.localdate(),
    ).first()


class ReservationCancelConfirmView(LoginRequiredMixin, View):
    template_name = "student/history/reservation_cancel_confirm.html"

    def get(self, request, pk):
        lesson = get_cancellable_lesson(request, pk)
        if lesson is None:
            messages.error(request, "このレッスンはキャンセルできません。")
            return redirect("reservation_history")
        trainer_info = get_object_or_404(TrainerInfo, user=lesson.trainer)
        return render(request, self.template_name, {
            "lesson": lesson,
            "trainer_pk": trainer_info.pk,
            "trainer_name": trainer_info.name,
            "lesson_price": trainer_info.lesson_fee,
        })

    def post(self, request, pk):
        updated = Lesson.objects.filter(
            pk=pk,
            student=request.user,
            lesson_status="reserved",
            lesson_date__gt=timezone.localdate(),
        ).update(
            student=None,
            lesson_status="available",
            reserved_lesson_type="",
        )

        if not updated:
            messages.error(request, "このレッスンはキャンセルできません。")
            return redirect("reservation_history")

        request.session["cancelled_lesson_id"] = pk
        return redirect("reservation_cancel_done")