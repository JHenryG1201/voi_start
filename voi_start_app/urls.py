from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage',),
    path('home_student', views.StudentHomeView.as_view(), name='student_home'),
    path('home_trainer', views.TrainerHomeView.as_view(), name='trainer_home'),
    path('ai_analysis', views.AIAnalysisView.as_view(), name='ai_analysis'),
    path('measurement', views.VoiceMeasurementView.as_view(), name='measurement'),
    path('analyze_voice', views.analyze_voice, name='analyze_voice'),
    path('analysis_result', views.AnalysisResultView.as_view(), name='analysis_result'),
    path('analysis_record', views.AnalysisRecordListView.as_view(), name='analysis_record'),
    path(
        'analysis_record_detail/<int:record_id>',
        views.AnalysisRecordDetailView.as_view(),
        name='analysis_record_detail',
    ),
    path('ai_question', views.ai_question),    
]