import redis
import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from .models import StoreTarsaction
from .serializers import TransactionSerializer
from .utils import get_url_from_content, generate_sig, get_url_from_content_result
from adds.models import Post, Subscription


# from adds.models import

class Success(APIView):
    def get(self, request):
        data1 = str(request)
        id = data1.split('&')

        payment_id = id[1].split('=')[1]
        data = dict(
            pg_merchant_id=535456,
            pg_payment=payment_id,
            pg_salt='some',

        )
        method = 'get_status2.php'
        payment = generate_sig(data, method)
        params = payment
        base_url = 'https://api.paybox.money/'
        r = requests.post(f"{base_url}{method}", params=params)
        date = 'pg_create_date'
        date = get_url_from_content_result(r.content, date)
        transaction = StoreTarsaction.objects.get(pk=int(payment_id))
        transaction.date = date
        transaction.save(update_fields=["date"])

        data = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        pk_post = data.get('pk')
        pk_subscription = data.get('pn')


        post = Post.objects.get(pk=pk_post.decode('utf-8'))
        subscription = Subscription.objects.get(pk=pk_subscription.decode('utf-8'))
        post.subscription = subscription
        # print('---------')
        post.save(update_fields=["subscription"])

        for i in StoreTarsaction.objects.all():
            val = i.date
            if val == None:
                i.delete()
        data.close()
        return HttpResponse(r.headers)


class Failure(APIView):
    def get(self, requests):
        return HttpResponse('Провал')


class Payment(APIView):

    def get(self, request, pk, pn, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('404')

        post = Post.objects.get(pk=pk)
        method = 'init_payment.php'

        sub = Subscription.objects.filter(pk=pn).values('price')
        price = int(sub[0]['price'])

        data = dict(
            pg_order_id=id,
            pg_merchant_id=535456,
            pg_amount=price,
            pg_description='some',
            pg_success_url='http://188.225.83.42:8011/api/v1/success',
            pg_salt='some',
        )

        payment = generate_sig(data, method)
        params = payment
        base_url = 'https://api.paybox.money/'
        r = requests.post(f"{base_url}{method}", params=params)
        url = get_url_from_content(r.content)
        payment_id = 'pg_payment_id'
        payment = get_url_from_content_result(r.content, payment_id)
        subscription = Subscription.objects.get(pk=pn)
        type_adversment = subscription.choice
        title = post.title
        user = str(request.user)
        print(user)
        user = User.objects.get(email=user)
        StoreTarsaction.objects.create(id=payment, title=title,
                                       type_adverments=type_adversment,
                                       user=user, price=price)
        data = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        data.mset({'pk': pk})
        data.mset({'pn': pn})
        data.close()
        return Response({'redirect': url})


class TransactionView(APIView):
    def get(self, request):
        user = str(request.user)
        user_obj = User.objects.get(email=user)
        queryset = StoreTarsaction.objects.all().filter(user=user_obj)
        serializer = TransactionSerializer(queryset, many=True).data
        return Response({'transaction': serializer})