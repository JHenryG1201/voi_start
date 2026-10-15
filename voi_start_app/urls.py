from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage',),
    path('home_student', views.StudentHomeView.as_view(), name='student_home'),
    path('home_trainer', views.TrainerHomeView.as_view(), name='trainer_home'),
]