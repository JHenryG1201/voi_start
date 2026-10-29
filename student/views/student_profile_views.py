from django.views.generic import DetailView
from django.shortcuts import redirect

from .student_profile_edit_views import StudentOnlyMixin
from student.models import StudentInfo

class StudentProfileView(StudentOnlyMixin, DetailView):
    model = StudentInfo
    template_name = "student/profile/student_profile.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "student_profile"):
            return redirect("student_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return self.request.user.student_profile