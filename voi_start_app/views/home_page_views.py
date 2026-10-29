from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import AccountType
from trainer.models import TrainerInfo
from student.models import StudentInfo

class HomePageView(TemplateView):
    template_name = 'common/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.account_type == AccountType.TRAINER:
                return redirect('trainer_home')
            return redirect('student_home')
        return super().dispatch(request, *args, **kwargs)


class AccountHomeView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            login_required=True,
            user_role=self.request.user.account_type,
            user_name=self.request.user.get_username(),
            user_initial=self.request.user.get_username()[:1].upper(),
        )
        return context


class StudentHomeView(AccountHomeView):
    template_name = 'student/home_student.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.account_type != AccountType.STUDENT:
            return redirect('trainer_home')
        if request.user.is_authenticated and not StudentInfo.objects.filter(user=request.user).exists():
            return redirect('student_profile_create')
        return super().dispatch(request, *args, **kwargs)


class TrainerHomeView(AccountHomeView):
    template_name = 'trainer/home_trainer.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.account_type != AccountType.TRAINER:
            return redirect('student_home')
        if request.user.is_authenticated and not TrainerInfo.objects.filter(user=request.user).exists():
            return redirect('trainer_profile_create')
        return super().dispatch(request, *args, **kwargs)