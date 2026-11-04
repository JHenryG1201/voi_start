from django.views.generic import TemplateView

class ReservationManagementView(TemplateView):
    template_name = "trainer/reservation/reservation_management.html"