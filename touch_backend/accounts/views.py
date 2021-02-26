from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cards.models import Card


class PagePathView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        resp = {}
        try:
            page_path = request.user.card.page_path
            resp['page_id'] = request.user.card.id
            resp['page_path'] = page_path
        except Card.DoesNotExist:
            resp['error'] = 'У этого пользователя нет визитки'
        return Response(resp, status=status.HTTP_200_OK)
