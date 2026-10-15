from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import AccountType


Account = get_user_model()


class HomePageViewTests(TestCase):
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

    def test_anonymous_user_sees_index_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')

    def test_logged_in_student_is_redirected_to_student_home(self):
        self.client.force_login(self.student)

        response = self.client.get('/')

        self.assertRedirects(response, '/home_student')

    def test_logged_in_trainer_is_redirected_to_trainer_home(self):
        self.client.force_login(self.trainer)

        response = self.client.get('/')

        self.assertRedirects(response, '/home_trainer')
