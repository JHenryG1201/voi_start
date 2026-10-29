from .measurement_views import VoiceMeasurementView
from .ai_analysis_views import AIAnalysisView, analysis_status, analyze_voice
from .analysis_result_views import AnalysisResultView
from .analysis_record_views import AnalysisRecordListView
from .analysis_record_detail_views import AnalysisRecordDetailView
from .trainer_list_views import TrainerListView
from .trainer_detail_views import TrainerDetailView
from .student_profile_edit_done_views import StudentProfileEditDoneView
from .student_profile_edit_views import StudentInfoCreateView, StudentProfileEditView
from .student_profile_views import StudentProfileView

__all__ = [
    "VoiceMeasurementView",
    "AIAnalysisView",
    "analysis_status",
    "analyze_voice",
    "AnalysisResultView",
    "AnalysisRecordListView",
    "AnalysisRecordDetailView",
    "TrainerListView",
    "TrainerDetailView",
    "StudentProfileEditDoneView",
    "StudentProfileEditView",
    "StudentInfoCreateView",
    "StudentProfileView",
]