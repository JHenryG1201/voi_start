from django.views.generic import ListView
from trainer.models import TrainerInfo

class TrainerListView(ListView):
    model = TrainerInfo
    template_name = "student/trainer_list/trainer_list.html"
    context_object_name = "trainers"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()

        trainer_name = self.request.GET.get("trainer_name", "").strip()
        genre = self.request.GET.get("genre", "").strip()

        if trainer_name:
            queryset = queryset.filter(name__icontains=trainer_name)

        if genre:
            queryset = queryset.filter(speciality_genre=genre)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trainer_name"] = self.request.GET.get("trainer_name", "").strip()
        context["genre"] = self.request.GET.get("genre", "").strip()
        context["genre_choices"] = TrainerInfo.GENRE
        return context