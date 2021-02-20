from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    page_url = models.URLField()
    photo = models.ImageField(blank=True)
    inst_url = models.URLField(blank=True)
    vk_url = models.URLField(blank=True)
    teleg_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(max_length=2048, blank=True)

    def __str__(self) -> str:
        return f'Визитка {self.owner}'

    def last_name(self):
        return self.owner.last_name

    def first_name(self):
        return self.owner.first_name
