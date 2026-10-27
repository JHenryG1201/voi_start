from django.views.generic import DetailView

from trainer.models import TrainerInfo

class TrainerDetailView(DetailView):
    model = TrainerInfo
    template_name = "student/trainer_list/trainer_detail.html"
    context_object_name = "trainer"