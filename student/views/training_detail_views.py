from django.views.generic import DetailView

from student.models import Training

class TrainingDetailView(DetailView):
    model = Training
    template_name = "student/training/training_detail.html"
    context_object_name = "training"