from django.views.generic import DeleteView
from django.urls import reverse

from trainer.models import Lesson

class AvailabeSlotDeleteView(DeleteView):
    model = Lesson
    template_name = 'trainer/reservation/available_slot_delete.html'

    def get_success_url(self):
        return reverse('available_slot_delete_done')