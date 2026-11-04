from django.views.generic import CreateView
from django.urls import reverse

from trainer.models import Lesson
from trainer.forms import ReservationSlotCreateForm

class ReservationSlotCreateView(CreateView):
    model = Lesson
    form_class = ReservationSlotCreateForm
    template_name = "trainer/reservation/reservation_slot_create.html"

    def get_success_url(self):
        return reverse('reservation_slot_create_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.trainer = self.request.user
        return super().form_valid(form)