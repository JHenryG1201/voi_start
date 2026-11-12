from django import forms

from .models import StudentInfo, Feedback

MAX_AUDIO_MB = 20

class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ("name", "age", "sex", "speciality_genre", "goal", "low_note", "high_note")
        widgets = {
            "name": forms.TextInput(attrs={"class": "pe-input", "placeholder": "名前を入力"}),
            "age": forms.NumberInput(attrs={"class": "pe-input", "min": 1, "placeholder": "年齢を入力", "oninput": "validity.valid||(value='');"}),
            "sex": forms.Select(attrs={"class": "pe-input"}),
            "speciality_genre": forms.Select(attrs={"class": "pe-input"}),
            "low_note": forms.TextInput(attrs={"class": "pe-input", "placeholder": "低音を入力"}),
            "high_note": forms.TextInput(attrs={"class": "pe-input", "placeholder": "高音を入力"}),
            "goal": forms.Textarea(attrs={"class": "pe-input pe-area", "placeholder": "目標を入力"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields["speciality_genre"]

        choices = [c for c in field.choices if c[0] != ""]
        field.choices = [("", "選択してください")] + choices

        if not self.instance.pk:
            self.initial["speciality_genre"] = ""

class FeedbackRequestForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["audio"]
        widgets = {
            "audio": forms.ClearableFileInput(attrs={"accept": "audio/*", "class": "fu-file-input"}),
            # "content": forms.Textarea(attrs={"rows": 6, "placeholder": "フィードバック依頼内容を書いてください"}),
        }

    def clean_audio(self):
        audio = self.cleaned_data["audio"]
        if audio.size > MAX_AUDIO_MB * 1024 * 1024:
            raise forms.ValidationError(f"Audio must be {MAX_AUDIO_MB}MB or smaller.")
        return audio