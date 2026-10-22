from django.urls import path
from . import views

urlpatterns = [
    path('ai_analysis', views.AIAnalysisView.as_view(), name='ai_analysis'),
    path('measurement', views.VoiceMeasurementView.as_view(), name='measurement'),
    path('analyze_voice', views.analyze_voice, name='analyze_voice'),
    path('analysis_result', views.AnalysisResultView.as_view(), name='analysis_result'),
    path('analysis_record', views.AnalysisRecordListView.as_view(), name='analysis_record'),
    path('analysis_record_detail/<int:record_id>', views.AnalysisRecordDetailView.as_view(), name='analysis_record_detail',),  
    path("analysis/<int:record_id>/status/", views.analysis_status, name="analysis_status"),
]
