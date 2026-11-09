from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from trainer.models import Lesson, TrainerInfo

class ReservationConfirmView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.session.get("reservation")
        if not data or not data.get("paid"):
            return redirect("trainer_list")
        lesson = get_object_or_404(Lesson, pk=data["lesson_id"])
        trainer_info = get_object_or_404(TrainerInfo, user=lesson.trainer)
        return render(request, "student/trainer_list/reservation/reservation_confirm.html", {
            "lesson": lesson,
            "trainer_pk": trainer_info.pk,
            "trainer_name": trainer_info.name,
            "lesson_price": trainer_info.lesson_fee,
        })

    def post(self, request):
        data = request.session.get("reservation")
        if not data or not data.get("paid"):
            return redirect("trainer_list")

        with transaction.atomic():
            updated = Lesson.objects.filter(
                pk=data["lesson_id"],
                lesson_status="available",
            ).update(
                student=request.user,
                lesson_status="reserved",
                reserved_lesson_type=data["lesson_type"],
            )

        if updated == 0:
            messages.error(request, "申し訳ありません。この枠はすでに予約されました。")
            return redirect("trainer_list")

        request.session["completed_lesson_id"] = data["lesson_id"]
        del request.session["reservation"]
        return redirect("reservation_done")