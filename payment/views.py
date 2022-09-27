import redis
import requests
from django.http import HttpResponse
from rest_framework import viewsets, response, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from .models import Payment, StoreTarsaction
from .serializers import PaymentSerializer, PostSubscription, TransactionSerializer
from .utils import generate_sig, get_url_from_content, generate_sig2, get_url_from_content_result
from adds.models import Post, Subscription
from rest_framework import generics

# from adds.models import


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['post', ]

    def create(self, request, pk, *args, **kwargs):
        print(pk, '______________')
        post = Post.objects.get(pk=pk)
        serializer = PostSubscription(post, many=False).data

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        payment = request.data
        method = 'init_payment.php'

        payment = dict(payment)
        payment['id'] = obj.id

        payment = generate_sig(payment, method)
        params = payment
        base_url = 'https://api.paybox.money/'
        r = requests.post(f"{base_url}{method}", params=params)
        assert 200 == r.status_code
        url = get_url_from_content(r.content)
        return response.Response({"redirect": url}, status=status.HTTP_200_OK)


class api(APIView):
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
        payment = generate_sig2(data, method)

        params = payment
        base_url = 'https://api.paybox.money/'
        r = requests.post(f"{base_url}{method}", params=params)
        assert 200 == r.status_code

        date = 'pg_create_date'
        date = get_url_from_content_result(r.content, date)
        transaction = StoreTarsaction.objects.get(pk=int(payment_id))
        transaction.date = date
        transaction.save(update_fields=["date"])

        data = redis.Redis()
        pk_post = data.get('pk')
        pk_subscription = data.get('pn')
        pk_sub = pk_post.decode('utf-8')
        print(pk_post,'97896gn...............')
        post = Post.objects.get(pk=pk_post.decode('utf-8'))
        subscription=Subscription.objects.get(pk=pk_subscription.decode('utf-8'))
        post.subscription = subscription
        post.save(update_fields=["subscription"])

        # post.save(update_fields=["date"])
        print(pk_post.decode('utf-8'),'------1')

        for i in StoreTarsaction.objects.all():
            val=i.date
            if val==None:
                i.delete()


        return HttpResponse(r.headers)


class api2(APIView):
    def get(self, requests):
        print(requests.headers)
        return HttpResponse('Провал')








class Payment(APIView):
    def get(self, request, pk, pn, *args, **kwargs):

        post = Post.objects.get(pk=pk)
        serializer = PostSubscription(post, many=False).data

        method = 'init_payment.php'
        obj_subsription = Post.objects.filter(pk=pk).values('subscription')
        sub = Subscription.objects.filter(pk=pn).values('price')
        price = int(sub[0]['price'])
        data = dict(
            pg_order_id=id,
            pg_merchant_id=535456,
            pg_amount=price,
            pg_description='some',
            pg_success_url='http://127.0.0.1:8000/api/success',
            pg_salt='some',

        )

        payment = generate_sig2(data, method)
        params = payment
        base_url = 'https://api.paybox.money/'
        r = requests.post(f"{base_url}{method}", params=params)
        assert 200 == r.status_code
        url = get_url_from_content(r.content)

        payment_id = 'pg_payment_id'
        payment = get_url_from_content_result(r.content, payment_id)

        subscription = Subscription.objects.get(pk=pn)
        type_adversment = subscription.choice
        title = post.title
        user=str(request.user)
        user=user.split()[2]
        user=User.objects.get(email=user)
        StoreTarsaction.objects.create(id=payment, title=title,
                                       type_adverments=type_adversment,
                                       user=user,price=price)

        # bytes({'pk': pk, 'pn': pn}
        data = redis.Redis()
        payment=str(payment)
        ids=[pk,pn]
        ids=bytes(ids)
        data.mset({'pk':pk})
        data.mset({'pn':pn})

        return Response({'redirect': url})


class TransactionView(APIView):
    def get(self,request):

        user = str(request.user)
        user = user.split()[2]
        user_obj = User.objects.get(email=user)
        queryset = StoreTarsaction.objects.all().filter(user=user_obj)
        print(queryset)
        serializer =TransactionSerializer(queryset,many=True).data
        return Response({'transaction':serializer})
