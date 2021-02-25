from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class RetrieveUpdateCardView(generics.RetrieveUpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'page_path'

    def check_object_permissions(self, request, obj):
        if request.method != 'GET':
            if (request.user != obj.owner):
                self.permission_denied(
                        request,
                        message='Визитка другого человека',
                        code='403'
                    )
        return super().check_object_permissions(request, obj)


class CreateFieldView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FieldSerializer

    def perform_create(self, serializer):
        serializer.save(card=self.request.user.card)


class UpdateFieldView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FieldSerializer
    queryset = Field.objects.all()

    def check_object_permissions(self, request, obj):
        if (request.user != obj.card.owner):
            self.permission_denied(
                    request,
                    message='Поле из чужой визитки',
                    code='403'
                )
        return super().check_object_permissions(request, obj)
