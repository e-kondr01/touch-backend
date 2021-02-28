from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from cards.models import Card


@receiver(post_save, sender=User, dispatch_uid="create_card")
def create_card(sender, instance, created, **kwargs):
    if created:
        new_card = Card(owner=instance, page_path=instance.username)
        new_card.save()
