from django.contrib.auth import get_user_model


from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import Token

from adds.models import Category, Subcategory, City, Subscription, Post, ReviewPost

User = get_user_model()


class TestAdds(APITestCase):
    def setUp(self):

        self.user_test = User.objects.create(email='test@test.com', password='qwerty12345')
        # self.user_token = Token.objects.create(user=self.user_1)
        self.category = Category.objects.create(title='Transport', icon_image='abc.png')
        self.subcategory = Subcategory.objects.create(category=self.category, title='Auto')
        self.subscription = Subscription.objects.create(choice='VIP', price=100)
        self.city = City.objects.create(title='Batken', slug='Batken')

        self.post = Post.objects.create(category=self.category,
                                        subcategory=self.subcategory, city=self.city,
                                        title='Mazda',
                                        description='excellent', from_price=100, to_price=200,
                                        image='abc.png', email='test@test.com',
                                        phone_number='+996555444333', wa_number='+996555444333',
                                        is_activated=True, status='in_progress')

        self.data = {
           'category': 'RealEstate', 'subcategory': 'Tower',
            'city': 'Osh', 'title': 'TimTimov',
            'description': 'WOW', 'from_price': 100, 'to_price': 200,
            'image': 'abc.jpeg', 'email': 'a@a.com', 'phone_number': '+996555333444',
            'wa_number': '+996555999888', 'is_activated': True, 'status': 'in_progress'
        }

    # def test_category(self):
    #     self.test = Category.objects.create(title='RealEstate', icon_image='abc.png')
    #     response = self.client.get(reverse('category'))
    #     self.assertEqual(response.data['count'], 2)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_subcategory(self):
    #     self.test = Subcategory.objects.create(category=self.category, title='Tank')
    #     response = self.client.get(reverse('subcategory'))
    #     self.assertEqual(response.data['count'], 2)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_subscription(self):
    #     self.test = Subscription.objects.create(choice='urgent', price=500)
    #     response = self.client.get(reverse('subscription'))
    #     self.assertEqual(response.data['count'], 2)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_city(self):
    #     self.test = City.objects.create(title='Bishkek', slug='Bishkek')
    #     response = self.client.get(reverse('city'))
    #     self.assertEqual(response.data['count'], 2)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_post_list(self):
    #     response = self.client.get(reverse('postlist'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_post_listdate(self):
    #     response = self.client.get(reverse('postlistdate'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_mypost(self):
    #     response = self.client.get(reverse('mypost'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_review(self):
    #     self.test = ReviewPost.objects.create(email='a@a.com', title='Mers', text='wow', post=self.post)
    #     response = self.client.get(reverse('mypost'))
    #     self.assertEqual(response.data['count'], 1)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_create_post_invalid_user(self):
    #     data = self.data.copy()
    #     client = APIClient()
    #     url = reverse('createpost')
    #     response = client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, 401)


    # def test_filtering_by_price(self):
    #     client = APIClient()
    #     url = reverse('postlist')
    #     params = {'price_from': 8500}
    #     response = client.get(url, params)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data['results']), 1)




    # def authenticate(self):
    #     self.client.post(reverse('register'), {
    #         'username': 'username',
    #         'email': 'email@email.com',
    #         'password': 'adminemail',
    #         'password_confirm': 'adminemail'})
    #     user.is_active = True
    #     user.save()
    #     response = self.client.post(reverse('login'), {
    #         'email': 'email@email.com',
    #         'password': 'adminemail',
    #         })
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["token"]}')
    #
    # def test_create_post_validu_ser(self):
    #     self.authenticate()
    #     data = self.data.copy()
    #     response =self.client.post(reverse('createpost'), data, format='json')
    #     self.assertEqual(response.status_code, 201)

    # def test_create_post_valid_user(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token.key)
    #     response = self.client.post(reverse('createpost'), self.data, format='json')
    #     self.assertEqual(response.status_code, 201)



