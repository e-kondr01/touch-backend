from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO

from .models import Card


@receiver(post_save, sender=Card)
def generate_new_sticker(sender, instance: Card,
                         created: bool, **kwargs) -> None:
    """Генерируем стикер, если у карточки его нет"""
    if not instance.qr:
        qr_img = instance.generate_qr_code()
        qr_io = BytesIO()
        qr_img.save(qr_io, "JPEG", quality=85)
        qr = File(qr_io, name=f"qr_{instance.pk}")
        instance.qr = qr
        instance.save()
