from django.db.models import Max
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
    serializer_class = CreateFieldSerializer

    def perform_create(self, serializer):
        '''У созданного поля должен быть
        последний порядковый номер '''
        max_order = Field.objects.filter(
            card=self.request.user.card
        ).aggregate(Max('order'))[
            'order__max'
        ]
        if not max_order:
            max_order = 0
        serializer.save(
            card=self.request.user.card,
            order=max_order+1
            )


class UpdateDestroyFieldView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveUpdateFieldSerializer
    queryset = Field.objects.all()

    def check_object_permissions(self, request, obj):
        if (request.user != obj.card.owner):
            self.permission_denied(
                    request,
                    message='Поле из чужой визитки',
                    code='403'
                )
        return super().check_object_permissions(request, obj)

    def perform_destroy(self, instance):
        order = instance.order
        card = instance.card
        instance.delete()
        fields = card.fields.filter(
            order__gt=order)
        '''Двигаем порядок'''
        for field in fields:
            field.order -= 1
            field.save()
