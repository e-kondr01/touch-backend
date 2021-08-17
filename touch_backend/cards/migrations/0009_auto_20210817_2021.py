from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0008_auto_20210512_2116"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="has_changed_username",
            field=models.BooleanField(
                default=False, verbose_name="менял логин")
        ),
        migrations.AddField(
            model_name="card",
            name="qr",
            field=models.ImageField(blank=True, null=True, upload_to="",
                                    verbose_name="QR код"),
        ),
    ]
