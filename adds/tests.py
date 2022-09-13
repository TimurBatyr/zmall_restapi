from django.contrib.auth import get_user_model
from unittest import mock

from faker.providers import file
from rest_framework.test import APITestCase
from django.urls import reverse

from adds.models import Category, Subcategory, City, Subscription

User = get_user_model()


class TestAdds(APITestCase):
    def setUp(self):
        mock_file = mock.MagicMock(spec=file)
        mock_file.name = 'photo.jpg'

        self.user_test = User.objects.create(username='Test', password='qwerty12345', is_active=True)

        self.category = Category.objects.create(title='Transport', icon_image='abc.png')
        self.subcategory = Subcategory.objects.create(category=self.category, title='Auto')
        self. subscription = Subscription.objects.create(choice='VIP', price=100)


    def test_category(self):
        self.test = Category.objects.create(title='RealEstate', icon_image='abc.png')
        response = self.client.get(reverse('category'))
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, 200)

    # def test_subcategory(self):
    #    response = self.client.get(reverse('subcategory'))
    #    self.assertEqual(response.status_code, 200)
    #
    # def test_city(self):
    #    response = self.client.get(reverse('city'))
    #    self.assertEqual(response.status_code, 200)
    #
    # def test_subscription(self):
    #    response = self.client.get(reverse('subscription'))
    #    self.assertEqual(response.status_code, 200)