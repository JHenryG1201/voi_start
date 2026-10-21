
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

#     prompt = f"""
# You are a careful and encouraging singing and voice-practice coach.

# Analyze the following audio features and produce personalized advice.

# USER PREFERENCES
# - Response language: {preferred_language}

# AUDIO ANALYSIS DATA
# {analysis_json}

# RULES
# 1. Explain what the numerical features suggest, without pretending
#    that numerical features alone can reveal everything about voice quality.
# 2. Explain pitch range and median pitch in plain language.
# 3. Do not interpret stability_score without acknowledging that its
#    meaning depends on the application's scoring algorithm.
# 4. RMS is signal amplitude and depends on recording conditions.
# 5. Spectral features and MFCCs are not direct measurements of beauty,
#    singing skill, health, or emotional expression.
# 6. The recording may be too short to determine the user's full range.
# 7. Recommend songs as starting points, not guaranteed vocal matches.
#    Do not invent exact song keys, singer ranges, or technical facts.
#    Mention that the user should transpose songs if needed.
# 8. Recommend gentle, beginner-friendly exercises. Tell the user to
#    stop if they experience pain, persistent hoarseness, or dizziness.
# 9. Do not diagnose a medical condition.
# 10. Be specific, constructive, realistic, and encouraging.

# Return valid JSON only in Japanese, using exactly this structure:
# {{
#   "overall_summary": "short summary",
#   "tone_quality": {{
#     "observations": ["observation 1", "observation 2"],
#     "possible_strengths": ["strength 1"],
#     "areas_to_practice": ["area 1"],
#     "confidence": "low, medium, or high",
#     "limitations": ["limitation 1"]
#   }},
#   "pitch_analysis": {{
#     "observed_range": "plain-language explanation",
#     "median_pitch": "plain-language explanation",
#     "stability_interpretation": "cautious explanation"
#   }},
#   "song_recommendations": [
#     {{
#       "title": "song title",
#       "artist": "artist",
#       "reason": "why it may suit the user",
#       "difficulty": "beginner, intermediate, or advanced",
#       "singing_tip": "practical tip"
#     }}
#   ],
#   "training_plan": [
#     {{
#       "exercise": "exercise name",
#       "duration_minutes": 5,
#       "instructions": ["step 1", "step 2"],
#       "purpose": "what it practices"
#     }}
#   ],
#   "next_recording_tips": ["tip 1", "tip 2"],
#   "disclaimer": "A short explanation of the limitations of this analysis."
# }}

# Provide 3 to 5 song recommendations and 3 to 5 exercises.
# """
    prompt = f"""
あなたは、丁寧で励まし上手な歌唱・発声練習コーチです。以下の音声分析データをもとに、ユーザーに合わせた具体的なアドバイスを日本語で提供してください。

## ユーザー設定
- 回答言語：{preferred_language}

## 音声分析データ
{analysis_json}

## 分析ルール

1. 数値的な特徴から推測できることを、分かりやすく説明してください。ただし、数値だけで実際の声質や歌唱力を完全に判断できるかのような表現は避けてください。
2. ピッチの範囲と中央値について、専門知識がない人にも理解できるように説明してください。
3. stability_score（安定性スコア）を解釈するときは、アプリケーション独自の計算方法や評価アルゴリズムによって意味が異なることを必ず考慮してください。
4. RMSは音声信号の振幅を表す値であり、録音音量、マイクとの距離、録音環境などの影響を受けます。RMSだけで声の大きさや声量の強さを断定しないでください。
5. スペクトル特徴量やMFCCは音声の音響的な特徴を表すものであり、それらの数値だけで声の美しさ、歌唱技術、健康状態、感情表現などを直接評価しないでください。
6. 録音時間が短い場合、ユーザーの本来の音域や歌唱能力を十分に判断できない可能性があることを説明してください。
7. 曲の推薦は、あくまで練習を始めるための候補として提示してください。実際の声に必ず合うと断定せず、正確な楽曲キー、歌手の音域、専門的な音楽情報を根拠なく作り出さないでください。歌いにくい場合は、自分の声に合わせてキーを変更（移調）するように勧めてください。
8. 初心者でも無理なく取り組める、優しい発声練習を提案してください。痛み、長引く声のかすれ、めまいなどが生じた場合は、練習を中止するように伝えてください。
9. 音声データから病気や医学的な状態を診断しないでください。
10. 具体的で実践しやすく、現実的で前向きなアドバイスを提供してください。改善点を伝える際も、否定的・断定的な表現を避けてください。

## 声質（tone_quality）の表現ルール

声質については、専門用語や数値を並べるだけでなく、ユーザーが実際の音をイメージできるように、擬音語・擬態語・日常的な表現を積極的に使用してください。

ただし、これらの表現は音声分析データから推測できる範囲で慎重に使用してください。音声を直接聴いていない場合、聴感上の特徴を断定せず、「〜の可能性があります」「実際の聴感による確認が必要です」といった表現を使用してください。

### 1. 高音域の表現

- 「シャカシャカ」：軽く、細かく、やや薄い印象の音。ただし、高周波成分が多いことだけで、このような聴感を断定しないでください。
- 「キラキラ」：明るく、輝きのある印象の音。高周波成分や倍音の特徴だけで、実際の輝きや透明感を断定しないでください。
- 「刺さる」：高音が強く、鋭く、耳に刺激的に感じられる音。スペクトルの特徴だけで耳への刺激を断定しないでください。
- 「抜けがよい」：音がこもらず、明瞭に聴こえる印象。
- 「キンキン」：高音が鋭く、強調されているように感じられる音。実際の聴感を確認できない場合は、断定しないでください。

### 2. 低音域の表現

- 「ズンズン」：低音に厚みや響きがあり、存在感を感じる音。
- 「ドンドン」：低音に迫力や力強さを感じる音。
- 「こもった音」：音の輪郭が不明瞭で、抜けが悪いように感じられる音。
- 「ボワボワ」：低音が広がりすぎて、輪郭がぼやけているように感じられる音。
- 「深みがある」：落ち着きや厚みを感じる音。ただし、低いピッチだけで深みがあると断定しないでください。

### 3. 中音域・ボーカル全体の表現

- 「クリア」：音の輪郭がはっきりしていて、明瞭に聴こえる印象。
- 「埋もれる」：伴奏や周囲の音に対して、ボーカルが聴こえにくい状態。ボーカル単独の音声データだけでは、伴奏に埋もれるかどうかを判断しないでください。
- 「艶（つや）がある」：滑らかで、豊かさや響きが感じられる声の印象。音響特徴量だけで艶の有無を断定しないでください。
- 「ハリがある」：声に芯や張りが感じられる印象。
- 「ふんわり」：柔らかく、優しい印象の音。
- 「スカスカ」：音の厚みや密度が少なく感じられる状態。ただし、録音品質の影響も考慮してください。
- 「まとまりがある」：音の特徴が比較的均一で、まとまって聴こえる印象。安定性スコアだけで断定しないでください。

### 4. 声質の評価に関する追加ルール

- すべての擬音語を無理に使用せず、データに根拠がある表現だけを選んでください。
- 「高周波成分が比較的多い」などの音響的な観察と、「キラキラして聴こえる可能性がある」などの聴感上の推測を区別してください。
- ピッチの高さだけで「キラキラ」「刺さる」「艶がある」などの声質を決めつけないでください。
- RMSが大きいだけで「迫力がある」「ハリがある」と判断しないでください。
- MFCCやスペクトルの数値だけで「声が美しい」「歌が上手い」と評価しないでください。
- 音声分析データだけでは判断できない項目は、無理に評価せず、判断できない理由を簡潔に説明してください。
- 改善点は欠点として断定せず、「今後の練習で意識するとよい点」として伝えてください。
- 分析の信頼度は「low」「medium」「high」のいずれかで示し、その理由をlimitationsに記載してください。
- confidenceは指定された英語の値を使用してください。

## 出力形式

有効なJSONのみを日本語で返してください。JSONの前後にMarkdown、コードブロック、追加の説明を付けないでください。

キー名とデータ構造は、以下の形式を厳密に守ってください。

{{
  "overall_summary": "分析結果の短いまとめ",
  "tone_quality": {{
    "observations": [
      "音声データから観察できる特徴と、対応する擬音語・感覚的な表現"
    ],
    "possible_strengths": [
      "強みとして考えられる点"
    ],
    "areas_to_practice": [
      "今後の練習で意識するとよい点"
    ],
    "confidence": "low、medium、highのいずれか",
    "limitations": [
      "分析の限界や、実際に聴いて確認する必要がある点"
    ]
  }},
  "pitch_analysis": {{
    "observed_range": "観測された音域についての分かりやすい説明",
    "median_pitch": "ピッチの中央値についての分かりやすい説明",
    "stability_interpretation": "安定性スコアの意味と解釈上の注意点"
  }},
  "song_recommendations": [
    {{
      "title": "曲名",
      "artist": "アーティスト名",
      "reason": "この曲が練習候補になる理由",
      "difficulty": "beginner、intermediate、advancedのいずれか",
      "singing_tip": "具体的な歌い方のアドバイス"
    }}
  ],
  "training_plan": [
    {{
      "exercise": "練習名",
      "duration_minutes": 5,
      "instructions": [
        "練習手順1",
        "練習手順2"
      ],
      "purpose": "この練習で身につけたいこと"
    }}
  ],
  "next_recording_tips": [
    "次回の録音で意識すること"
  ],
  "disclaimer": "音声分析の限界についての短い説明"
}}

## 推薦数と練習メニュー

- song_recommendationsは3～5曲にしてください。
- training_planは3～5種類の練習にしてください。
- 各練習のduration_minutesには、実際に取り組みやすい練習時間を数値で指定してください。
- 各練習は初心者でも無理なく取り組める内容にしてください。
- 楽曲は音域や歌い方の特徴を考慮した候補を選び、必要に応じて移調を勧めてください。
- データが不十分な場合でも、根拠のない声質の断定はせず、分析上の制約を明確にしたうえで、一般的に取り組みやすい候補を提案してください。
- JSONとして正しく解析できるように、文字列内の二重引用符は適切にエスケープし、末尾のカンマは使用しないでください。
- 出力は必ずJSONとして解析可能な形式にしてください。
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
