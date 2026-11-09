from django.views.generic import TemplateView

class HistoryView(TemplateView):
    template_name = "student/history/history.html"