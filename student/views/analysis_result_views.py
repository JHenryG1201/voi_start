from django.shortcuts import get_object_or_404

from voi_start_app.views import AccountHomeView
from student.models import VoiceAnalysisRecord

class AnalysisResultView(AccountHomeView):
    template_name = "student/ai/analysis_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record_id = self.request.GET.get("record")
        if record_id:
            context["record"] = get_object_or_404(
                VoiceAnalysisRecord,
                pk=record_id,
                user=self.request.user,
            )
        return context