# Generated by Django 5.0.4 on 2024-07-01 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0018_room_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='estado',
            field=models.CharField(choices=[('activa', 'Activa'), ('eliminada', 'Eliminada')], default='activa', max_length=10),
        ),
    ]
