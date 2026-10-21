import json
import logging
import time

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "tone_quality": {
            "type": "object",
            "properties": {
                "observations": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["observations"],
        },
        "song_recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "artist": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["title", "artist", "reason"],
            },
        },
        "training_plan": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "exercise": {"type": "string"},
                    "duration_minutes": {"type": "integer"},
                    "instructions": {"type": "array", "items": {"type": "string"}},
                    "purpose": {"type": "string"},
                },
                "required": ["exercise", "duration_minutes", "instructions", "purpose"],
            },
        },
    },
    "required": ["tone_quality", "song_recommendations", "training_plan"],
}


def _compact(value):
    """Round floats and drop long numeric arrays (e.g. MFCC frames) to keep the prompt short."""
    if isinstance(value, float):
        return round(value, 3)
    if isinstance(value, dict):
        return {k: _compact(v) for k, v in value.items()}
    if isinstance(value, list):
        if len(value) > 8:
            return None
        return [_compact(v) for v in value]
    return value


def _drop_none(value):
    if isinstance(value, dict):
        return {k: _drop_none(v) for k, v in value.items() if v is not None}
    return value


def generate_voice_coaching_report(analysis_data):
    """Generate voice coaching feedback from audio-analysis features (a dict)."""

    if isinstance(analysis_data, str):
        analysis_data = json.loads(analysis_data)
    if not isinstance(analysis_data, dict):
        raise ValueError("analysis_data must be a dictionary")

    analysis_json = json.dumps(
        _drop_none(_compact(analysis_data)),
        ensure_ascii=False,
    )

    prompt = f"""あなたは、丁寧で励まし上手な歌唱・発声練習コーチです。以下の音声分析データをもとに、初心者向けのアドバイスを日本語で作ってください。

## 音声分析データ
{analysis_json}

## ルール
- 数値だけで声質・歌唱力・健康状態を断定せず、「〜の可能性があります」と表現する。
- RMSは録音環境の影響を受ける。stability_scoreの意味はアプリ独自の計算方法に依存する。
- スペクトル特徴量やMFCCだけで声の美しさや歌唱技術を評価しない。
- 録音が短い場合は、音域を十分に判断できない可能性に触れる。
- 病気や医学的な状態は診断しない。痛み・長引くかすれ・めまいがあれば練習を中止するよう伝える。
- 曲は練習の候補として挙げ、キーや歌手の音域など不確かな情報を作らない。歌いにくければ移調を勧める。
- 前向きで具体的に書く。

## 声質の表現
データに根拠がある場合だけ、次のような擬音語・日常的な表現を1〜2個使う。聴感は断定しない。
- 高音域: キラキラ、シャカシャカ、抜けがよい、キンキン
- 低音域: ズンズン、ドンドン、こもった、深みがある
- 中音域: クリア、ハリがある、艶がある、ふんわり
音響的な観察と聴感上の推測を区別し、判断できない点はその理由を短く述べる。

## 出力
JSONのみを返してください（説明やコードブロックは不要）。形式は次のとおりです。
{{"tone_quality": {{"observations": ["声質の観察（2文以内）"]}}, "song_recommendations": [{{"title": "曲名", "artist": "アーティスト名", "reason": "理由（1文）"}}], "training_plan": [{{"exercise": "練習名", "duration_minutes": 5, "instructions": ["手順1", "手順2"], "purpose": "目的（1文）"}}]}}

- song_recommendationsは3件、training_planは3件。
- instructionsは各2手順まで。各文は短くする。
"""

    base_url = settings.OLLAMA_BASE_URL.rstrip("/")
    model = settings.OLLAMA_MODEL

    started = time.monotonic()
    response = requests.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You generate cautious, structured voice-coaching reports as valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            "format": REPORT_SCHEMA,   # if Ollama returns HTTP 400, change this to "json"
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "num_ctx": 4096,
                "num_predict": 1500,   # a cap, not a target: generation stops when the JSON is complete
                "temperature": 0.3,
            },
        },
        timeout=(10, 300),             # (connect, read)
    )
    response.raise_for_status()
    data = response.json()

    logger.info(
        "ollama: %.1fs, prompt_tokens=%s, output_tokens=%s, done_reason=%s",
        time.monotonic() - started,
        data.get("prompt_eval_count"),
        data.get("eval_count"),
        data.get("done_reason"),
    )

    content = data["message"]["content"]
    try:
        report = json.loads(content)
    except json.JSONDecodeError:
        logger.error("Invalid JSON from model (done_reason=%s): %s", data.get("done_reason"), content)
        raise

    # Make sure the shapes tasks.py relies on are there.
    tone = report.get("tone_quality", {})
    observations = tone.get("observations")
    if isinstance(observations, str):
        tone["observations"] = [observations]
    if not tone.get("observations"):
        raise ValueError("Model response is missing tone_quality.observations")
    report["tone_quality"] = tone

    for key in ("song_recommendations", "training_plan"):
        if not isinstance(report.get(key), list) or not report[key]:
            raise ValueError(f"Model response is missing {key}")

    return report