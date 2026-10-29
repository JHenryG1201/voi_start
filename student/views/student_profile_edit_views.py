from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

from accounts.models import AccountType
from student.models import StudentInfo
from student.forms import StudentInfoForm

class StudentOnlyMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.account_type != AccountType.STUDENT:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class StudentInfoCreateView(StudentOnlyMixin, CreateView):
    model = StudentInfo
    form_class = StudentInfoForm
    template_name = "student/profile/student_profile_edit.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "student_profile"):
            return redirect("student_profile")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('student_profile_edit_done')}?{urlencode({'mode': 'create'})}"

class StudentProfileEditView(StudentOnlyMixin, UpdateView):
    model = StudentInfo
    form_class = StudentInfoForm
    template_name = "student/profile/student_profile_edit.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "student_profile"):
            return redirect("student_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return self.request.user.student_profile

    def get_success_url(self):
        return f"{reverse('student_profile_edit_done')}?{urlencode({'mode': 'edit'})}"