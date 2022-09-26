from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .index import pusher_client

from .serializers import MessageSerializer


class MessageAPIView(APIView):
    '''Chat between seller and customer'''
    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        # chat = f'{message.id}'
        # message = serializer.message
        pusher_client.trigger('message', 'message', {
            'sender': message.sender.id,
            'receiver': message.receiver.id,
            'message': message.message
        })

        return Response({'success': 'success'})