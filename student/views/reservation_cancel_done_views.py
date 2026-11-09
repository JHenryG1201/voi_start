from django.views.generic import TemplateView

class ReservationCancelDoneView(TemplateView):
    template_name = "student/history/reservation_cancel_done.html"