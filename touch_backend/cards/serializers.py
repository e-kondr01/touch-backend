from rest_framework import serializers

from .models import *


class CreateFieldSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False)
    # Порядок должен быть в response, но не в request body.

    class Meta:
        model = Field
        fields = ['id', 'title', 'value', 'link', 'order']


class RetrieveUpdateFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'title', 'value', 'link', 'order']

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
    fields = RetrieveUpdateFieldSerializer(many=True, required=False)

    class Meta:
        model = Card
        fields = [
            'id', 'displayed_name', 'page_path', 'photo',
            'color_one', 'color_two',
            "has_changed_username",
            "redirect_url",
            'fields'
        ]
        read_only_fields = ['fields']

    def update(self, instance, validated_data):
        '''Удаляем старую пикчу'''
        if 'photo' in validated_data:
            instance.photo.delete()
        return super().update(instance, validated_data)


class QRSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "qr"
        ]
