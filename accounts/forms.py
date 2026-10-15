from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

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

    def save(self, commit=True):
        account = super().save(commit=False)
        account.account_type = self.cleaned_data['user_type']
        if commit:
            account.save()
            self.save_m2m()
        return account


class AccountAuthenticationForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        label="利用者を選択してください",
        choices=(
            ("student", "生徒"),
            ("trainer", "トレーナー"),
        ),
        widget=forms.RadioSelect,
    )

    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        selected_type = cleaned_data.get('user_type')

        if user is not None and selected_type != user.account_type:
            raise ValidationError(
                "選択した利用者の種類とアカウントが一致しません。",
                code='invalid_login',
            )

        return cleaned_data