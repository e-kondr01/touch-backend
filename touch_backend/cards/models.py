from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name='владелец')

    '''page_path надо добавить после
    {{host}}/cards/ , чтобы получить ссылку
    на страницу, и после
    {{host}}/api/cards/ , чтобы получить
    ссылку на запрос, отдающий JSON
    с информацией '''
    page_path = models.CharField(
        verbose_name='ссылка на страницу',
        unique=True,
        max_length=128)
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

    class Meta:
        verbose_name = "визитка"
        verbose_name_plural = "визитки"


class Field(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='fields',
        verbose_name='визитка')
    title = models.CharField(
        max_length=64, verbose_name='название')
    value = models.CharField(
        max_length=1024,
        verbose_name='значение')
    link = models.URLField(
        verbose_name='ссылка',
        blank=True)
    order = models.PositiveSmallIntegerField(
        verbose_name='порядок в списке'
    )

    def __str__(self) -> str:
        return f'{self.title} из {self.card}'

    class Meta:
        verbose_name = "поле"
        verbose_name_plural = "поля"
        ordering = ['order']
