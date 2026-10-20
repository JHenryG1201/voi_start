from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError
from .audio_analysis import analyze_audio

from django.conf import settings
from accounts.models import AccountType
from .models import VoiceAnalysisRecord

import json
import logging
logger = logging.getLogger(__name__)

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

def build_tone_summary(features: dict) -> str:
    tone = features["tone"]
    pitch = features["pitch"]

    if tone["spectral_centroid_hz"] > 2500:
        brightness = "明るく前に出る"
    else:
        brightness = "落ち着いた"

    if pitch["stability_score"] >= 0.65:
        stability = "音程が安定しています"
    else:
        stability = "音程の安定性を伸ばせます"

    return f"{brightness}声です。{stability}。"


def recommend_songs(features: dict) -> list[str]:
    low_note = features["pitch"]["low_note"]
    high_note = features["pitch"]["high_note"]

    # Replace this with a database query based on song vocal ranges.
    return [
        f"現在の音域 {low_note}〜{high_note} に合う曲A",
        "中音域を活かせる曲B",
    ]


def recommend_training(features: dict) -> list[str]:
    training = []

    if features["pitch"]["stability_score"] < 0.65:
        training.append("ピアノ音に合わせてロングトーンを行う")

    if features["loudness"]["dynamic_range"] < 0.02:
        training.append("小さい声から大きい声へ段階的に発声する")

    if not training:
        training.append("リップロールを1日3分行う")

    return training

# @login_required
# def analyze_voice(request):
#     if request.method == "GET":
#         return redirect("measurement")
#     if request.method != "POST":
#         return JsonResponse({"error": "POSTメソッドのみ利用できます。"}, status=405)

#     audio = request.FILES.get("audio")
#     if not audio:
#         return JsonResponse({"error": "音声ファイルがありません。"}, status=400)
#     if audio.size > 25 * 1024 * 1024:
#         return JsonResponse({"error": "録音は25MB以下にしてください。"}, status=413)

#     allowed_types = {"audio/webm", "audio/ogg", "audio/wav", "audio/mp4", "audio/mpeg"}
#     content_type = (audio.content_type or "").split(";", 1)[0].lower()
#     if content_type and content_type not in allowed_types:
#         return JsonResponse({"error": "対応していない音声形式です。"}, status=415)

#     # webm_data = audio.read();
#     # audio_file = AudioSegment.from_file(
#     #     io.BytesIO(webm_data),
#     #     format="webm"
#     # )

#     # audio_file = audio_file.set_channels(1)
#     # audio_file = audio_file.set_frame_rate(16000)
#     # audio_file = audio_file.set_sample_width(2)

#     # wav_buffer = io.BytesIO()
#     # audio_file.export(wav_buffer, format="wav")
#     # wav_buffer.seek(0)

#     with transaction.atomic():
#         record = VoiceAnalysisRecord.objects.create(
#             user = request.user,
#             audio = audio,
#             song_name = request.POST.get("song_name", "")[:255]
#         )
#         try:
#             audio_features = analyze_audio(record.audio.path)
#             pitch = audio_features["pitch"]
#             record.low_note = pitch["low_note"] or [""]
#             record.high_note = pitch["high_note"] or ""
#             record.tone_quality = build_tone_summary(audio_features)
#             record.recommended_songs = recommend_songs(audio_features)
#             record.recommended_training = recommend_training(audio_features)

#             # result = _build_analysis()
#             # record.low_note = result["low_note"]
#             # record.high_note = result["high_note"]
#             # record.tone_quality = result["tone_quality"]
#             # record.recommended_songs = result["recommended_songs"]
#             # record.recommended_trainings = result["recommended_trainings"]

#             record.save()
#         except (ValidationError, ValueError, OSError) as exc:
#             record.status = "failed"
#             record.error_message = str(exc)
#             record.save(update_fields=("status", "error_message"))
#             return JsonResponse({"error": "音声分析に失敗しました。"}, status=422)

#     return JsonResponse({
#         "record_id": record.pk,
#         "redirect_url": f"/analysis_result?record={record.pk}",
#     })

@login_required
def analyze_voice(request):
    if request.method == "GET":
        return redirect("measurement")

    if request.method != "POST":
        return JsonResponse(
            {"error": "POSTメソッドのみ利用できます。"},
            status=405,
        )

    audio = request.FILES.get("audio")

    if not audio:
        return JsonResponse(
            {"error": "音声ファイルがありません。"},
            status=400,
        )

    if audio.size == 0:
        return JsonResponse(
            {"error": "音声ファイルが空です。"},
            status=400,
        )

    if audio.size > 25 * 1024 * 1024:
        return JsonResponse(
            {"error": "録音は25MB以下にしてください。"},
            status=413,
        )

    allowed_types = {
        "audio/webm",
        "audio/ogg",
        "audio/wav",
        "audio/mp4",
        "audio/mpeg",
        "application/octet-stream",
    }

    content_type = (audio.content_type or "").split(";", 1)[0].lower()

    if content_type and content_type not in allowed_types:
        return JsonResponse(
            {"error": f"対応していない音声形式です: {content_type}"},
            status=415,
        )

    try:
        with transaction.atomic():
            record = VoiceAnalysisRecord.objects.create(
                user=request.user,
                audio=audio,
                song_name=request.POST.get("song_name", "")[:255],
            )

            audio_features = analyze_audio(record.audio.path)
            pitch = audio_features["pitch"]

            record.low_note = pitch["low_note"] or ""
            record.high_note = pitch["high_note"] or ""
            record.tone_quality = build_tone_summary(audio_features)
            record.recommended_songs = recommend_songs(audio_features)
            # record.recommended_training = recommend_training(audio_features)
            record.recommended_trainings = json.dumps(audio_features)
            record.save()

    except Exception as exc:
        logger.exception("Voice analysis failed")

        # Show diagnostic details during development only.
        message = str(exc) if settings.DEBUG else "音声分析に失敗しました。"

        return JsonResponse(
            {
                "error": "音声分析に失敗しました。",
                "detail": message,
            },
            status=422,
        )

    return JsonResponse({
        "record_id": record.pk,
        "redirect_url": f"/analysis_result?record={record.pk}",
    })