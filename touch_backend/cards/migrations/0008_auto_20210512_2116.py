# Generated by Django 3.1.7 on 2021-05-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_auto_20210303_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='color_one',
            field=models.CharField(default='#005eff', max_length=16, verbose_name='цвет 1'),
        ),
        migrations.AddField(
            model_name='card',
            name='color_two',
            field=models.CharField(default='#4508d4', max_length=16, verbose_name='цвет 2'),
        ),
    ]
