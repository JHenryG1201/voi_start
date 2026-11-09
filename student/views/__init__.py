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
from .training_list_views import TrainingListView
from .training_detail_views import TrainingDetailView
from .reservation_select_views import ReservationSelectView
from .reservation_payment_views import ReservationPaymentView
from .reservation_confirm_views import ReservationConfirmView
from .reservation_done_views import ReservationDoneView

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
    "TrainingListView",
    "TrainingDetailView",
    "ReservationSelectView",
    "ReservationPaymentView",
    "ReservationConfirmView",
    "ReservationDoneView",
]