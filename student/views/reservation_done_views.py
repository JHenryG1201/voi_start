from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, render, get_object_or_404

from trainer.models import Lesson, TrainerInfo

class ReservationDoneView(LoginRequiredMixin, View):
    def get(self, request):
        lesson_id = request.session.get("completed_lesson_id")
        if not lesson_id:
            return redirect("trainer_list")
        lesson = get_object_or_404(Lesson, pk=lesson_id, student=request.user)        
        trainer_info = get_object_or_404(TrainerInfo, user=lesson.trainer)
        return render(request, "student/trainer_list/reservation/reservation_done.html", {
            "lesson": lesson,
            "trainer_pk": trainer_info.pk,
            "trainer_name": trainer_info.name,
            "lesson_price": trainer_info.lesson_fee,
        })