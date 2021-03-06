# Generated by Django 3.1.5 on 2021-01-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210126_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='turn_num',
            field=models.IntegerField(default=1, verbose_name='Номер хода'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='turn',
            name='turn_time',
            field=models.PositiveIntegerField(blank=True, default=30, verbose_name='Время хода'),
        ),
    ]
