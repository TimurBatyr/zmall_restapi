from rest_framework.response import Response
from rest_framework.views import APIView
from .index import pusher_client


class ChatAPIView(APIView):

    def post(self, request):
        pusher_client.trigger('zmall_chat', 'message', {
            'username': request.data['username'],
            'message': request.data['message']
        })

        return Response([])