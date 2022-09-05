from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .index import pusher_client

from .serializers import MessageSerializer


class MessageAPIView(APIView):
    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = serializer.message
        pusher_client.trigger('zmall_chat', 'message', {
            'sender': message.sender,
            'receiver': message.receiver,
            'message': message.message
        })

        return Response({'success': 'success'})
