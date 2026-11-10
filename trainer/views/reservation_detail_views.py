from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from trainer.models import Lesson

class ReservationDetailView(LoginRequiredMixin, DetailView):
    template_name = "trainer/reservation/reservation_detail.html"
    model = Lesson
    context_object_name = "lesson"
    