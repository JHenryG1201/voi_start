from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import AccountType


Account = get_user_model()


class AccountAuthenticationTests(TestCase):
    def setUp(self):
        self.student = Account.objects.create_user(
            username='student1',
            password='correct-password',
            account_type=AccountType.STUDENT,
        )
        self.trainer = Account.objects.create_user(
            username='trainer1',
            password='correct-password',
            account_type=AccountType.TRAINER,
        )

    def test_student_login_redirects_to_student_home(self):
        response = self.client.post(
            '/login',
            {
                'username': 'student1',
                'password': 'correct-password',
                'user_type': AccountType.STUDENT,
            },
        )

        self.assertRedirects(response, '/home_student')
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.pk)

    def test_trainer_login_redirects_to_trainer_home(self):
        response = self.client.post(
            '/login',
            {
                'username': 'trainer1',
                'password': 'correct-password',
                'user_type': AccountType.TRAINER,
            },
        )

        self.assertRedirects(response, '/home_trainer')

    def test_login_rejects_matching_credentials_with_wrong_account_type(self):
        response = self.client.post(
            '/login',
            {
                'username': 'student1',
                'password': 'correct-password',
                'user_type': AccountType.TRAINER,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '選択した利用者の種類とアカウントが一致しません。',
        )
        self.assertNotIn('_auth_user_id', self.client.session)


class AccountRegistrationTests(TestCase):
    def test_registration_persists_selected_account_type(self):
        response = self.client.post(
            '/accounts/register',
            {
                'username': 'new-trainer',
                'password1': 'a-strong-password',
                'password2': 'a-strong-password',
                'user_type': AccountType.TRAINER,
            },
        )

        self.assertRedirects(response, '/accounts/register_scuccess')
        self.assertEqual(
            Account.objects.get(username='new-trainer').account_type,
            AccountType.TRAINER,
        )
