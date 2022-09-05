from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import UserProfile
from .index import pusher_client
from .models import Message
from .serializers import UserSerializer, MessageSerializer


@api_view(["GET",])
def user_list(request, pk=None):
    if request.method == 'GET':
        if pk:
            users = UserProfile.objects.filter(id=pk)
        else:
            users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, )


@api_view(["POST", "GET"])
def message_list(request):
    if request.method == 'GET':
        sender = request.user
        messages = Message.objects.filter(Q(sender_id=sender,)|Q (receiver_id=sender,))
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return Response(serializer.data, )

    elif request.method == 'POST':
        data = request.data
        serializer = MessageSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChatAPIView(APIView):

    def post(self, request):
        pusher_client.trigger('zmall_chat', 'message', {
            'username': request.data['username'],
            'message': request.data['message']
        })

        return Response([])