from django import forms
from django.utils import timezone
import logging

from .models import TrainerInfo, Lesson

logger = logging.getLogger(__name__)

class TrainerInfoForm(forms.ModelForm):
    class Meta:
        model = TrainerInfo
        fields = ("name", "age", "sex", "area", "contacts", "career", "speciality_genre", "comment", "feedback_fee", "lesson_fee",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "pe-input", "placeholder": "名前を入力"}),
            "age": forms.NumberInput(attrs={"class": "pe-input", "min": 1, "placeholder": "年齢を入力", "oninput": "validity.valid||(value='');"}),
            "sex": forms.Select(attrs={"class": "pe-input"}),
            "area": forms.TextInput(attrs={"class": "pe-input", "placeholder": "活動地を入力"}),
            "contacts": forms.TextInput(attrs={"class": "pe-input", "placeholder": "問い合わせ先を入力"}),
            "career": forms.Textarea(attrs={"class": "pe-input pe-area", "placeholder": "経歴を入力"}),
            "speciality_genre": forms.Select(attrs={"class": "pe-input"}),
            "comment": forms.Textarea(attrs={"class": "pe-input pe-area", "placeholder": "コメントを入力"}),
            "feedback_fee": forms.NumberInput(attrs={"class": "pe-input", "min": 0, "step": 1, "placeholder": "例：1000", "oninput": "validity.valid||(value='');"}),
            "lesson_fee": forms.NumberInput(attrs={"class": "pe-input", "min": 0, "step": 1, "placeholder": "例：5000", "oninput": "validity.valid||(value='');"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields["speciality_genre"]

        choices = [c for c in field.choices if c[0] != ""]
        field.choices = [("", "選択してください")] + choices

        if not self.instance.pk:
            self.initial["speciality_genre"] = ""

class ReservationSlotCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = {"lesson_date", "lesson_start_time", "lesson_end_time", "lesson_type"}
        widgets = {
            "lesson_date": forms.DateInput(
                attrs={"class": "rsc-input", "type": "date", "min": timezone.localdate().isoformat(),}, 
                format="%Y-%m-%d",
            ),
            "lesson_start_time": forms.TimeInput(attrs={"class": "rsc-input", "type": "time"}),
            "lesson_end_time": forms.TimeInput(attrs={"class": "rsc-input", "type": "time"}),
            "lesson_type": forms.RadioSelect(choices=Lesson.LESSON_TYPE, attrs={"class": "rsc-radio"}),        
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()

        lesson_date = cleaned_data.get("lesson_date")
        start_time = cleaned_data.get("lesson_start_time")
        end_time = cleaned_data.get("lesson_end_time")

        if start_time and end_time:
            if end_time <= start_time:
                self.add_error(
                    "lesson_end_time",
                    "終了時間は開始時間より後に設定してください。"
                )

        if lesson_date and start_time and end_time:
            overlapping_lessons = Lesson.objects.filter(
                trainer=self.user,
                lesson_date=lesson_date,
                lesson_start_time__lt=end_time,
                lesson_end_time__gt=start_time,
            )
            logger.warning(overlapping_lessons.count())
            logger.warning(lesson_date)

            if self.instance.pk:
                overlapping_lessons = overlapping_lessons.exclude(
                    pk=self.instance.pk
                )

            if overlapping_lessons.exists():
                self.add_error(
                    "lesson_start_time",
                    "この時間帯には別のレッスンが登録されています。"
                )

        return cleaned_data