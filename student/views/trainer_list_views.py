from django.views.generic import ListView
from django.db.models import OuterRef, Subquery, Sum, Count, Case, When, FloatField, F
from django.db.models.functions import Coalesce, Cast

from trainer.models import LessonReview, FeedbackReview, TrainerInfo

class TrainerListView(ListView):
    model = TrainerInfo
    template_name = "student/trainer_list/trainer_list.html"
    context_object_name = "trainers"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()

        lesson_stats = (
            LessonReview.objects
            .filter(lesson__trainer=OuterRef("user"))
            .values("lesson__trainer")
            .annotate(total=Sum("rating"), cnt=Count("id"))
        )
        feedback_stats = (
            FeedbackReview.objects
            .filter(feedback__trainer=OuterRef("user"))
            .values("feedback__trainer")
            .annotate(total=Sum("rating"), cnt=Count("id"))
        )

        queryset = queryset.annotate(
            lesson_total=Coalesce(Subquery(lesson_stats.values("total")[:1]), 0),
            lesson_cnt=Coalesce(Subquery(lesson_stats.values("cnt")[:1]), 0),
            feedback_total=Coalesce(Subquery(feedback_stats.values("total")[:1]), 0),
            feedback_cnt=Coalesce(Subquery(feedback_stats.values("cnt")[:1]), 0),
        ).annotate(
            review_count=F("lesson_cnt") + F("feedback_cnt"),
            avg_rating=Case(
                When(review_count=0, then=None),
                default=Cast(F("lesson_total") + F("feedback_total"), FloatField())
                        / Cast(F("review_count"), FloatField()),
                output_field=FloatField(),
            ),
        )

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