from rest_framework import generics

from .models import *
from .serializers import *


class CardView(generics.RetrieveUpdateAPIView):
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
