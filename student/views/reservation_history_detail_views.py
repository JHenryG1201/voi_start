from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from trainer.models import Lesson

class ReservationHistoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "student/history/reservation_history_detail.html"
    model = Lesson
    context_object_name = "lesson"
    