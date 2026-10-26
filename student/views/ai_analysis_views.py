from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse

from voi_start_app.views import AccountHomeView
from student.models import VoiceAnalysisRecord
from voi_start_app.tasks import run_voice_analysis

class AIAnalysisView(AccountHomeView):
    template_name = "student/ai/ai_analysis.html"

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

    record = VoiceAnalysisRecord.objects.create(
        user=request.user,
        audio=audio,
        song_name=request.POST.get("song_name", "")[:255],
        status="pending",
    )
    transaction.on_commit(lambda: run_voice_analysis.delay(record.pk))

    return JsonResponse(
        {
            "record_id": record.pk,
            "status_url": reverse("analysis_status", args=[record.pk]),
        },
        status=202,
    )

@login_required
def analysis_status(request, record_id):
    record = get_object_or_404(VoiceAnalysisRecord, pk=record_id, user=request.user)
    if record.status == "failed":
        return JsonResponse({"state": "failed", "error": "声が確認できませんでした"})
    if record.status == "complete":
        return JsonResponse({
            "state": "done",
            "redirect_url": f"/student/analysis_result?record={record.pk}",
        })
    return JsonResponse({"state": "pending"})