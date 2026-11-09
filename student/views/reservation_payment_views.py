from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render

from trainer.models import Lesson, TrainerInfo

class ReservationPaymentView(LoginRequiredMixin, View):
    def get(self, request):
        if "reservation" not in request.session:
            return redirect("trainer_list")
        lesson = get_object_or_404(Lesson, pk=request.session["reservation"]["lesson_id"])
        trainer_info = get_object_or_404(TrainerInfo, user=lesson.trainer)
        return render(request, "student/trainer_list/reservation/reservation_payment.html", {
            "lesson": lesson,
            "trainer_pk": trainer_info.pk,
            "trainer_name": trainer_info.name,
            "lesson_price": trainer_info.lesson_fee,
        })

    def post(self, request):
        data = request.session.get("reservation")
        if not data:
            return redirect("trainer_list")

        data["paid"] = True
        request.session["reservation"] = data
        return redirect("reservation_confirm")