from django.core.files import File
from django.db.models import Max
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from io import BytesIO

from .models import *
from .serializers import *
from .utilities import process_link


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
    permission_classes = [permissions.IsAuthenticated]
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

        if 'link' in serializer.validated_data:
            input = serializer.validated_data['link']
            type = serializer.validated_data['title']
            link = process_link(input=input, type=type)

            serializer.save(
                card=self.request.user.card,
                order=max_order+1,
                link=link
            )
        else:
            serializer.save(
                card=self.request.user.card,
                order=max_order+1
            )


class UpdateDestroyFieldView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
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

    def perform_update(self, serializer):
        if 'link' in serializer.validated_data:
            input = serializer.validated_data['link']
            if 'title' in serializer.validated_data:
                type = serializer.validated_data['title']
            else:
                type = self.get_object().title
            link = process_link(input=input, type=type)
            serializer.save(link=link)
        else:
            serializer.save()

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


class RetrieveQRView(generics.RetrieveAPIView):
    """View для получения QR"""
    queryset = Card.objects.all()
    serializer_class = QRSerializer
    lookup_field = "page_path"
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.qr:
            """Создаём QR"""
            qr_img = instance.generate_qr_code()
            qr_io = BytesIO()
            qr_img.save(qr_io, "JPEG", quality=85)
            qr = File(qr_io, name=f"qr_{instance.pk}")
            instance.qr = qr
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
