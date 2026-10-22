from django.shortcuts import get_object_or_404

from voi_start_app.views import AccountHomeView
from student.models import VoiceAnalysisRecord

class AnalysisRecordDetailView(AccountHomeView):
    template_name = "student/ai/analysis_record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["record"] = get_object_or_404(
            VoiceAnalysisRecord,
            pk = kwargs["record_id"],
            user = self.request.user,
        )
        return context
