from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError

from accounts.models import AccountType
from .models import VoiceAnalysisRecord

# Create your views here.
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
        return super().dispatch(request, *args, **kwargs)


class TrainerHomeView(AccountHomeView):
    template_name = 'trainer/home_trainer.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.account_type != AccountType.TRAINER:
            return redirect('student_home')
        return super().dispatch(request, *args, **kwargs)

class VoiceMeasurementView(AccountHomeView):
    template_name = "student/ai/measurement.html"

class AIAnalysisView(AccountHomeView):
    template_name = "student/ai/ai_analysis.html"

class AnalysisRecordListView(AccountHomeView):
    template_name = "student/ai/analysis_record.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = VoiceAnalysisRecord.objects.filter(user=self.request.user)
        return context

class AnalysisRecordDetailView(AccountHomeView):
    template_name = "student/ai/analysis_record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["record"] = get_object_or_404(
            VoiceAnalysisRecord,
            pk = kwargs["record_id"],
            user = self.request.user,
        )
        return context


class AnalysisResultView(AccountHomeView):
    template_name = "student/ai/analysis_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record_id = self.request.GET.get("record")
        if record_id:
            context["record"] = get_object_or_404(
                VoiceAnalysisRecord,
                pk=record_id,
                user=self.request.user,
            )
        return context

def _build_analysis():
    return {
        "low_note": "mid1G",
        "high_note": "hiC",
        "tone_quality": "明るく、息の成分が適度にある声です。中音域で安定しています。",
        "recommended_songs": ["曲名A", "曲名C"],
        "recommended_trainings": [
            "リップロールを1日3分行う",
            "無理のない音量で mid1G〜hiC をゆっくり発声する",
        ],
    }

@require_POST
@login_required
def analyze_voice(request):
    audio = request.FILES.get("audio")
    if not audio:
        return JsonResponse({"error": "音声ファイルがありません。"}, status=400)
    if audio.size > 25 * 1024 * 1024:
        return JsonResponse({"error": "録音は25MB以下にしてください。"}, status=413)

    allowed_types = {"audio/webm", "audio/ogg", "audio/wav", "audio/mp4", "audio/mpeg"}
    content_type = (audio.content_type or "").split(";", 1)[0].lower()
    if content_type and content_type not in allowed_types:
        return JsonResponse({"error": "対応していない音声形式です。"}, status=415)

    with transaction.atomic():
        record = VoiceAnalysisRecord.objects.create(
            user = request.user,
            audio = audio,
            song_name = request.POST.get("song_name", "")[:255]
        )
        try:
            result = _build_analysis()
            record.low_note = result["low_note"]
            record.high_note = result["high_note"]
            record.tone_quality = result["tone_quality"]
            record.recommended_songs = result["recommended_songs"]
            record.recommended_trainings = result["recommended_trainings"]
            record.save()
        except (ValidationError, ValueError, OSError) as exc:
            record.status = "failed"
            record.error_message = str(exc)
            record.save(update_fields=("status", "error_message"))
            return JsonResponse({"error": "音声分析に失敗しました。"}, status=422)

    return JsonResponse({
        "record_id": record.pk,
        "redirect_url": f"/analysis_result?record={record.pk}",
    })