from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

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

        if "username" in request.data:
            new_username = request.data["username"]
            user = request.user
            user.username = new_username
            user.save()

            card = user.card
            card.has_changed_username = True
            card.redirect_url = settings.HOST + new_username
            card.owner = None
            card.save()

            new_card = Card.objects.create(
                owner=request.user,
                page_path=new_username,
                photo=card.photo,
                displayed_name=card.displayed_name,
                color_one=card.color_one,
                color_two=card.color_two,
                has_changed_username=True,
                qr=card.qr
            )

            for field in card.fields.all():
                field.card = new_card
                field.save()

            resp = {}
            resp["new_username"] = new_username
            return Response(resp, status=status.HTTP_200_OK)

        else:
            detail = {}
            detail["error"] = "Provide username"
            raise ValidationError(detail=detail)


class IsUsernameUniqueView(APIView):
    """Проверка на уникальность username"""

    def post(self, request, *args, **kwargs):
        if "username" in request.data:
            username = request.data["username"]
            if Card.objects.filter(page_path=username):
                resp = {'username_status': 'taken'}
            else:
                resp = {'username_status': 'free'}
            return Response(resp, status=status.HTTP_200_OK)
        else:
            detail = {}
            detail["error"] = "Provide username"
            raise ValidationError(detail=detail)
