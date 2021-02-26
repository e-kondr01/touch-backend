from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'title', 'value', 'link', 'order']

    def create(self, validated_data):
        '''Изменяем порядок остальных полей '''
        fields = validated_data['card'].fields.filter(
            order__gte=validated_data['order']
        )
        for field in fields:
            field.order += 1
            field.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        '''Изменяем порядок остальных полей '''
        if 'order' in validated_data:
            new_order = validated_data['order']
            old_order = instance.order
            if new_order > old_order:
                fields = instance.card.fields.filter(
                    order__gt=old_order
                ).filter(
                    order__lte=new_order
                )
                for field in fields:
                    field.order -= 1
                    field.save()
            else:
                fields = instance.card.fields.filter(
                    order__gte=new_order
                ).filter(
                    order__lt=old_order
                )
                for field in fields:
                    field.order += 1
                    field.save()
        return super().update(instance, validated_data)


class CardSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, required=False)
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Card
        fields = ['id', 'owner', 'page_path', 'photo', 'delimiter', 'fields']
        read_only_fields = ['fields']

    def update(self, instance, validated_data):
        '''Удаляем старую пикчу'''
        instance.photo.delete()
        return super().update(instance, validated_data)
