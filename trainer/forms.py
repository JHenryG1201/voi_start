from django import forms
from .models import TrainerInfo

class TrainerInfoForm(forms.ModelForm):
    class Meta:
        model = TrainerInfo
        fields = ("name", "age", "sex", "area", "contacts", "career", "speciality_genre", "comment", "feedback_fee", "lesson_fee",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "pe-input", "placeholder": "名前を入力"}),
            "age": forms.NumberInput(attrs={"class": "pe-input", "placeholder": "年齢を入力"}),
            "sex": forms.Select(attrs={"class": "pe-input"}),
            "area": forms.TextInput(attrs={"class": "pe-input", "placeholder": "活動地を入力"}),
            "contacts": forms.TextInput(attrs={"class": "pe-input", "placeholder": "問い合わせ先を入力"}),
            "career": forms.Textarea(attrs={"class": "pe-input pe-area", "placeholder": "経歴を入力"}),
            "speciality_genre": forms.TextInput(attrs={"class": "pe-input", "placeholder": "得意ジャンルを入力"}),
            "comment": forms.Textarea(attrs={"class": "pe-input pe-area", "placeholder": "コメントを入力"}),
            "feedback_fee": forms.NumberInput(attrs={"class": "pe-input", "min": 0, "step": 1, "placeholder": "例：1000"}),
            "lesson_fee": forms.NumberInput(attrs={"class": "pe-input", "min": 0, "step": 1, "placeholder": "例：5000"}),
        }