from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cards.models import Card


class PageUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        resp = {}
        try:
            page_url = request.user.card.page_url
            resp['page_url'] = page_url
        except Card.DoesNotExist:
            resp['error'] = 'У этого пользователя нет визитки'
        return Response(resp, status=status.HTTP_200_OK)
