# Generated by Django 5.0.6 on 2024-05-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RealizarPublicacion', '0007_alter_fotopublicacion_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotopublicacion',
            name='foto',
            field=models.ImageField(upload_to='estatico/fotos_publicaciones/'),
        ),
    ]