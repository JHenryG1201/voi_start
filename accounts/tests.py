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

    def test_logged_in_user_is_available_on_follow_up_request(self):
        self.client.post(
            '/login',
            {
                'username': 'student1',
                'password': 'correct-password',
                'user_type': AccountType.STUDENT,
            },
        )

        response = self.client.get('/home_student')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user, self.student)

    def test_logout_clears_logged_in_user_and_redirects_to_index(self):
        self.client.force_login(self.student)

        response = self.client.post('/logout')

        self.assertRedirects(response, '/')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        homepage_response = self.client.get('/')
        self.assertEqual(homepage_response.status_code, 200)
        self.assertTemplateUsed(homepage_response, 'common/index.html')

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

    def test_same_username_logs_into_selected_account_type(self):
        trainer = Account.objects.create_user(
            username='shared-user',
            password='trainer-password',
            account_type=AccountType.TRAINER,
        )
        student = Account.objects.create_user(
            username='shared-user',
            password='student-password',
            account_type=AccountType.STUDENT,
        )

        response = self.client.post(
            '/login',
            {
                'username': 'shared-user',
                'password': 'trainer-password',
                'user_type': AccountType.TRAINER,
            },
        )

        self.assertRedirects(response, '/home_trainer')
        self.assertEqual(int(self.client.session['_auth_user_id']), trainer.pk)

        self.client.logout()
        response = self.client.post(
            '/login',
            {
                'username': 'shared-user',
                'password': 'student-password',
                'user_type': AccountType.STUDENT,
            },
        )

        self.assertRedirects(response, '/home_student')
        self.assertEqual(int(self.client.session['_auth_user_id']), student.pk)


class AccountRegistrationTests(TestCase):
    def test_registration_persists_selected_account_type(self):
        response = self.client.post(
            '/accounts/register',
            {
                'username': 'new-trainer@example.com',
                'password1': 'a-strong-password',
                'password2': 'a-strong-password',
                'user_type': AccountType.TRAINER,
            },
        )

        self.assertRedirects(response, '/accounts/register_scuccess')
        self.assertEqual(
            Account.objects.get(username='new-trainer@example.com').account_type,
            AccountType.TRAINER,
        )

    def test_different_account_types_can_use_the_same_username(self):
        common_data = {
            'username': 'shared@example.com',
            'password1': 'a-strong-password',
            'password2': 'a-strong-password',
        }

        student_response = self.client.post(
            '/accounts/register',
            {
                **common_data,
                'user_type': AccountType.STUDENT,
            },
        )
        trainer_response = self.client.post(
            '/accounts/register',
            {
                **common_data,
                'user_type': AccountType.TRAINER,
            },
        )

        self.assertRedirects(student_response, '/accounts/register_scuccess')
        self.assertRedirects(trainer_response, '/accounts/register_scuccess')
        self.assertEqual(
            Account.objects.filter(username='shared@example.com').count(),
            2,
        )

    def test_same_username_and_account_type_cannot_be_registered_twice(self):
        registration_data = {
            'username': 'duplicate-student@example.com',
            'password1': 'a-strong-password',
            'password2': 'a-strong-password',
            'user_type': AccountType.STUDENT,
        }

        first_response = self.client.post(
            '/accounts/register',
            registration_data,
        )
        second_response = self.client.post(
            '/accounts/register',
            {
                **registration_data,
            },
        )

        self.assertRedirects(first_response, '/accounts/register_scuccess')
        self.assertEqual(second_response.status_code, 200)
        self.assertContains(
            second_response,
            'A user with that username already exists.',
        )
