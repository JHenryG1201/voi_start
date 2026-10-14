from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

class AccountCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        label="利用者を選択してください",
        choices=(
            ("student", "生徒"),
            ("trainer", "トレーナー"),
        ),
        widget=forms.RadioSelect,
    )
    class Meta:
        model = Account
        fields = ('username', 'password1', 'password2')