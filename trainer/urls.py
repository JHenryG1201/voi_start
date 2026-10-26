from django.urls import path

from . import views

urlpatterns = [
    path("profile/create", views.TrainerInfoCreateView.as_view(), name="trainer_profile_create"),
    path("profile", views.TrainerProfileView.as_view(), name="trainer_profile"),
    path("profile/edit", views.TrainerProfileEditView.as_view(), name="trainer_profile_edit"),
]
