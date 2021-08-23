from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cards", "0009_auto_20210817_2021"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="redirect_url",
            field=models.URLField(
                blank=True, verbose_name="ссылка для редиректа")
        ),
        migrations.AlterField(
            model_name="card",
            name="owner",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL, verbose_name="владелец")
        )
    ]
