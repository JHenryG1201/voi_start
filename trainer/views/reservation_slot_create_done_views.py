from django.views.generic import TemplateView

class ReservationSlotCreateDoneView(TemplateView):
    template_name = 'trainer/reservation/reservation_slot_create_done.html'