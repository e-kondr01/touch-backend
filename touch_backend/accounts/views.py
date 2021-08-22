from django.contrib.auth import get_user_model
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
            resp['page_path'] = page_path
        except Card.DoesNotExist:
            resp['error'] = 'У этого пользователя нет визитки'
        return Response(resp, status=status.HTTP_200_OK)


class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """Меняем логин и сохраняем то, что пользователь его менял"""

        new_username = request.data["username"]
        user = request.user
        user.username = new_username
        user.save()

        card = user.card
        card.has_changed_username = True
        card.save()

        resp = {}
        resp["new_username"] = new_username
        return Response(resp, status=status.HTTP_200_OK)


class IsUsernameUniqueView(APIView):
    """Проверка на уникальность username"""

    def post(self, request, *args, **kwargs):
        user = get_user_model()
        username = request.data["username"]
        if user.objects.filter(username=username):
            resp = {'username_status': 'taken'}
        else:
            resp = {'username_status': 'free'}
        return Response(resp, status=status.HTTP_200_OK)
