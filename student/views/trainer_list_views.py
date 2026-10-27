from django.views.generic import ListView
from trainer.models import TrainerInfo

class TrainerListView(ListView):
    model = TrainerInfo
    template_name = "student/trainer_list/trainer_list.html"
    context_object_name = "trainers"