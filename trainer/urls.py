from django.urls import path

from . import views

urlpatterns = [
    path("profile/create", views.TrainerInfoCreateView.as_view(), name="trainer_profile_create"),
    path("profile", views.TrainerProfileView.as_view(), name="trainer_profile"),
    path("profile/edit", views.TrainerProfileEditView.as_view(), name="trainer_profile_edit"),
    path("profile/edit/done", views.TrainerProfileEditDoneView.as_view(), name="trainer_profile_edit_done"),
    path("reservation_management", views.ReservationManagementView.as_view(), name="reservation_management"),
    path("reservation_slot_create", views.ReservationSlotCreateView.as_view(), name="reservation_slot_create"),
    path("reservation_slot_create_done", views.ReservationSlotCreateDoneView.as_view(), name="reservation_slot_create_done"),  
    path("available_slots", views.AvailableSlotsView.as_view(), name="available_slots"),  
    path("available_slot_edit/<int:pk>", views.AvailableSlotEditView.as_view(), name="available_slot_edit"),
    path("available_slot_edit_done", views.AvailabeSlotEditDoneView.as_view(), name="available_slot_edit_done"),
    path("available_slot_delete/<int:pk>", views.AvailabeSlotDeleteView.as_view(), name="available_slot_delete"),
    path("available_slot_delete_done", views.AvailabeSlotDeleteDoneView.as_view(), name="available_slot_delete_done"),
    path("reservation_list", views.ReservationListView.as_view(), name="reservation_list"),
    path("reservation_list/<int:pk>", views.ReservationDetailView.as_view(), name="reservation_detail"),
]
