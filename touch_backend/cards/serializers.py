from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        '''это возможно убрать '''
        extra_kwargs = {
            'username': {'validators': []},
        }


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'title', 'value', 'link', 'order']


class CardSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, required=False)
    owner = UserSerializer()

    class Meta:
        model = Card
        fields = ['id', 'owner', 'page_path', 'photo', 'delimiter', 'fields']

    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner')
        fields_data = validated_data.pop('fields')

        instance.page_path = validated_data.get(
            'page_path', instance.page_path) # Тут нужно проверить уникальность
        instance.delimiter = validated_data.get(
            'delimiter', instance.delimiter)
        instance.save()

        owner = instance.owner

        owner.username = owner_data.get('username', owner.username)   # Тут нужно проверить уникальность
        owner.first_name = owner_data.get('first_name', owner.first_name)
        owner.last_name = owner_data.get('last_name', owner.last_name)
        owner.save()

        '''по полям пройтись'''


        return instance
