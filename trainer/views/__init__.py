from .trainer_profile_edit_views import TrainerProfileEditView, TrainerInfoCreateView
from .trainer_profile_views import TrainerProfileView
from .trainer_profile_edit_done_views import TrainerProfileEditDoneView
from .reservation_management_views import ReservationManagementView
from .reservation_slot_create_views import ReservationSlotCreateView
from .reservation_slot_create_done_views import ReservationSlotCreateDoneView
from .available_slots_views import AvailableSlotsView
from .available_slot_edit_views import AvailableSlotEditView
from .available_slot_edit_done_views import AvailabeSlotEditDoneView
from .available_slot_delete_views import AvailabeSlotDeleteView
from .available_slot_delete_done_views import AvailabeSlotDeleteDoneView

__all__ = [
    'TrainerProfileEditView',
    'TrainerInfoCreateView',
    'TrainerProfileView',
    'TrainerProfileEditDoneView',
    'ReservationManagementView',
    'ReservationSlotCreateView',
    'ReservationSlotCreateDoneView',
    'AvailableSlotsView',
    'AvailableSlotEditView',
    'AvailabeSlotEditDoneView',
    'AvailabeSlotDeleteView',
    'AvailabeSlotDeleteDoneView',
]