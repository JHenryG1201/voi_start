
import json
import requests

from django.conf import settings


def generate_voice_coaching_report(
    analysis_data,
    preferred_language="Japanese",
):
    """
    Generate voice coaching feedback from audio-analysis features.
    analysis_data should be a dictionary, not a JSON string.
    """

    if isinstance(analysis_data, str):
        analysis_data = json.loads(analysis_data)

    if not isinstance(analysis_data, dict):
        raise ValueError("analysis_data must be a dictionary")

    analysis_json = json.dumps(
        analysis_data,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
You are a careful and encouraging singing and voice-practice coach.

Analyze the following audio features and produce personalized advice.

USER PREFERENCES
- Response language: {preferred_language}

AUDIO ANALYSIS DATA
{analysis_json}

RULES
1. Explain what the numerical features suggest, without pretending
   that numerical features alone can reveal everything about voice quality.
2. Explain pitch range and median pitch in plain language.
3. Do not interpret stability_score without acknowledging that its
   meaning depends on the application's scoring algorithm.
4. RMS is signal amplitude and depends on recording conditions.
5. Spectral features and MFCCs are not direct measurements of beauty,
   singing skill, health, or emotional expression.
6. The recording may be too short to determine the user's full range.
7. Recommend songs as starting points, not guaranteed vocal matches.
   Do not invent exact song keys, singer ranges, or technical facts.
   Mention that the user should transpose songs if needed.
8. Recommend gentle, beginner-friendly exercises. Tell the user to
   stop if they experience pain, persistent hoarseness, or dizziness.
9. Do not diagnose a medical condition.
10. Be specific, constructive, realistic, and encouraging.

Return valid JSON only in Japanese, using exactly this structure:
{{
  "overall_summary": "short summary",
  "tone_quality": {{
    "observations": ["observation 1", "observation 2"],
    "possible_strengths": ["strength 1"],
    "areas_to_practice": ["area 1"],
    "confidence": "low, medium, or high",
    "limitations": ["limitation 1"]
  }},
  "pitch_analysis": {{
    "observed_range": "plain-language explanation",
    "median_pitch": "plain-language explanation",
    "stability_interpretation": "cautious explanation"
  }},
  "song_recommendations": [
    {{
      "title": "song title",
      "artist": "artist",
      "reason": "why it may suit the user",
      "difficulty": "beginner, intermediate, or advanced",
      "singing_tip": "practical tip"
    }}
  ],
  "training_plan": [
    {{
      "exercise": "exercise name",
      "duration_minutes": 5,
      "instructions": ["step 1", "step 2"],
      "purpose": "what it practices"
    }}
  ],
  "next_recording_tips": ["tip 1", "tip 2"],
  "disclaimer": "A short explanation of the limitations of this analysis."
}}

Provide 3 to 5 song recommendations and 3 to 5 exercises.
"""

    base_url = settings.OLLAMA_BASE_URL.rstrip("/")
    model = settings.OLLAMA_MODEL

    response = requests.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You generate cautious, structured voice-coaching "
                        "reports. Follow the requested JSON structure."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.3},
        },
        timeout=180,
    )
    response.raise_for_status()

    content = response.json()["message"]["content"]
    report = json.loads(content)

    return report
