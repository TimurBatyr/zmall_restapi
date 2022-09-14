from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User


class TestAccount(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.activate_url = reverse('activate')

        self.user_data = {
            'username': 'email',
            'email': 'email@email.com',
            'password': 'adminemail',
            'password_confirm': 'adminemail',
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestViews(TestAccount):
    def test_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_register_with_data(self):
        res = self.client.post(self.register_url, self.user_data)
        self.assertEqual(res.status_code, 201)

    def test_login_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_login_after_verification(self):
        user = User.objects.create_user(email='email@email.com', password="adminemail")
        user.is_active = True
        user.save()
        response = self.client.post(reverse('login'), {
            'email': 'email@email.com',
            'password': 'adminemail'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["tokens"]}')
        self.assertEqual(response.status_code, 200)



