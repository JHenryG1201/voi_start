from django.views.generic import ListView

from student.models import Training

class TrainingListView(ListView):
    model = Training
    template_name = "student/training/training_list.html"
    context_object_name = "trainings"
    paginate_by = 10
    ordering = ["title"]