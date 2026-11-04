from django.views.generic import UpdateView
from django.urls import reverse
from django.shortcuts import get_object_or_404

from trainer.models import Lesson
from trainer.forms import ReservationSlotCreateForm

class AvailableSlotEditView(UpdateView):
    model = Lesson
    form_class = ReservationSlotCreateForm
    template_name = "trainer/reservation/available_slot_edit.html"
    context_object_name = "lesson"

    def get_queryset(self):
        return Lesson.objects.filter(
            trainer=self.request.user
        )

    def get_success_url(self):
        return reverse('available_slot_edit_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs