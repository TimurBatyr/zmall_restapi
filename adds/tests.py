# from rest_framework.test import APITestCase
# from django.urls import reverse
#
# from adds.models import Category, Subcategory, City
#
#
# class TestAdds(APITestCase):
#     def setUp(self):
#         self.category = Category.objects.create(title='Transport', icon_image='abc.png')
#         Subcategory.objects.create(category=self.category, title='Auto')
#         City.objects.create(title='Batken')
#
#     def test_category(self):
#        response = self.client.get(reverse('category'))
#        self.assertEqual(response.status_code, 200)
#
#     def test_subcategory(self):
#        response = self.client.get(reverse('subcategory'))
#        self.assertEqual(response.status_code, 200)
#
#     def test_city(self):
#        response = self.client.get(reverse('city'))
#        self.assertEqual(response.status_code, 200)