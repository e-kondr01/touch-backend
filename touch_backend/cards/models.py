from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name='владелец')
    page_url = models.URLField(
        verbose_name='ссылка на страницу')
    photo = models.ImageField(
        blank=True, verbose_name='фото')
    delimiter = models.CharField(
        max_length=64, default='default',
        verbose_name='разделитель')

    def __str__(self) -> str:
        return f'Визитка {self.owner}'

    def last_name(self):
        return self.owner.last_name

    def first_name(self):
        return self.owner.first_name


class Field(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='fields',
        verbose_name='визитка')
    title = models.CharField(
        max_length=64, verbose_name='название')
    value = models.CharField(
        max_length=1024,
        verbose_name='значение')
    order = models.PositiveSmallIntegerField(
        verbose_name='порядок в списке'
    )

    def __str__(self) -> str:
        return f'{self.title} из {self.card}'
