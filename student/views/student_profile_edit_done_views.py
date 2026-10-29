from django.views.generic import TemplateView

from .student_profile_edit_views import StudentOnlyMixin

class StudentProfileEditDoneView(StudentOnlyMixin, TemplateView):
    template_name = 'student/profile/student_profile_edit_done.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["is_create"] = self.request.GET.get("mode") == "create"
        return ctx