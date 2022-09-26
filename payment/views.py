import requests

from rest_framework import viewsets, response, status
from decouple import config

from .models import Payment
from .serializers import PaymentSerializer
from .utils import generate_sig, get_url_from_content


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        payment = request.data
        method = 'init_payment.php'

        payment=dict(payment)
        payment['id'] = obj.id

        payment = generate_sig(payment, method)
        params = payment
        base_url = 'https://api.paybox.money/'
        r = requests.post(f"{base_url}{method}", params=params)
        assert 200 == r.status_code
        url = get_url_from_content(r.content)
        return response.Response({"redirect": url}, status=status.HTTP_200_OK)
