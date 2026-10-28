from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Account


class AccountCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "パスワードが一致していません",
    }
    
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
        

    def clean_username(self):
        return self.cleaned_data['username']

    def validate_unique(self):
        username = self.cleaned_data.get('username')
        account_type = self.cleaned_data.get('user_type')
        if (
            username
            and account_type
            and Account.objects.filter(
                username=username,
                account_type=account_type,
            ).exclude(pk=self.instance.pk).exists()
        ):
            self.add_error(
                'username',
                'このメールアドレスでアカウントが既に作成されています。',
            )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     account_type = cleaned_data.get('user_type')
    #     if Account.objects.filter(
    #         username=username,
    #         account_type=account_type,
    #     ).exists():
    #         raise forms.ValidationError(
    #             'このメールアドレスでアカウントが既に作成されています。',
    #         )
    #     return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        account.account_type = self.cleaned_data['user_type']
        if commit:
            account.save()
            self.save_m2m()
        return account


class AccountAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "メールアドレス、パスワード、または利用者の種類が正しくありません。"
        ),
        "inactive": "このアカウントは無効になっています。",
    }

    user_type = forms.ChoiceField(
        label="利用者を選択してください",
        choices=(
            ("student", "生徒"),
            ("trainer", "トレーナー"),
        ),
        widget=forms.RadioSelect,
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        selected_type = cleaned_data.get('user_type')
        matching_user = next(
            (
                account
                for account in Account.objects.filter(username=username)
                if account.check_password(password)
            ),
            None,
        )
        if matching_user and matching_user.account_type != selected_type:
            raise ValidationError('ユーザー名、パスワード、または利用者の種類が正しくありません。')
        user = (
            Account.objects
            .filter(username=username, account_type=selected_type)
            .first()
        )

        if user is None or not user.check_password(password):
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )

        self.confirm_login_allowed(user)
        self.user_cache = user
        return cleaned_data


class AccountDeletionForm(forms.Form):
    password = forms.CharField(
        label='現在のパスワード',
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('パスワードが正しくありません。')
        return password