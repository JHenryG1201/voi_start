from django.views.generic import ListView
from django.db.models import Sum, Count

from trainer.models import LessonReview, FeedbackReview

class EvaluationView(ListView):
    model = LessonReview
    template_name = "trainer/evaluation/evaluation.html"
    context_object_name = "lesson_reviews"

    def get_queryset(self):
        return LessonReview.objects.filter(lesson__trainer = self.request.user)

    @staticmethod
    def calc_average(lesson_reviews, feedback_reviews):
        lesson = lesson_reviews.aggregate(total=Sum("rating"), n=Count("id"))
        feedback = feedback_reviews.aggregate(total=Sum("rating"), n=Count("id"))

        total_rating = (lesson["total"] or 0) + (feedback["total"] or 0)
        total_count = lesson["n"] + feedback["n"]

        if total_count == 0:
            return 0
        return round(total_rating / total_count, 1)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_reviews = self.get_queryset()
        feedback_reviews = FeedbackReview.objects.filter(feedback__trainer=self.request.user)

        context["feedback_reviews"] = feedback_reviews
        context["average"] = self.calc_average(lesson_reviews, feedback_reviews)
        context["total"] = lesson_reviews.count() + feedback_reviews.count()
        return context
    