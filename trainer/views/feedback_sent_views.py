from django.views.generic import TemplateView

class FeedbackSentView(TemplateView):
    template_name = "trainer/feedback/feedback_sent.html"