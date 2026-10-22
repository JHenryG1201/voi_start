import logging
from celery import shared_task

from .audio_analysis import analyze_audio
from .voice_coach import generate_voice_coaching_report
from student.models import VoiceAnalysisRecord

logger = logging.getLogger(__name__)


@shared_task
def run_voice_analysis(record_id):
    record = VoiceAnalysisRecord.objects.get(pk=record_id)
    try:
        audio_features = analyze_audio(record.audio.path)
        pitch = audio_features["pitch"]
        report = generate_voice_coaching_report(
            audio_features
        )

        record.low_note = pitch["low_note"] or ""
        record.high_note = pitch["high_note"] or ""
        record.tone_quality = report["tone_quality"]["observations"][0]
        record.recommended_songs = report["song_recommendations"]
        record.recommended_trainings = report["training_plan"]
        record.status = "complete"
        record.save()
    except Exception as exc:
        logger.exception("Voice analysis failed")
        record.status = "failed"
        record.error_message = str(exc)
        record.save(update_fields=("status", "error_message"))