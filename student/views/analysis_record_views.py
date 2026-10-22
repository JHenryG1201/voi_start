from student.models import VoiceAnalysisRecord
from voi_start_app.views import AccountHomeView

class AnalysisRecordListView(AccountHomeView):
    template_name = "student/ai/analysis_record.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = VoiceAnalysisRecord.objects.filter(
            user=self.request.user, status="complete"
        )
        return context