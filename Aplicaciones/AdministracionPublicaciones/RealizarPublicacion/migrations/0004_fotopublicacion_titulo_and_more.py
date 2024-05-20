# Generated by Django 5.0.6 on 2024-05-20 04:51

import Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RealizarPublicacion', '0003_alter_publicacion_anio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotopublicacion',
            name='titulo',
            field=models.CharField(default=Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models.FotoPublicacion.default_title, max_length=50),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='tipo_embarcacion',
            field=models.CharField(choices=[('barco', 'Barco'), ('velero', 'Velero'), ('yate', 'Yate'), ('lancha', 'Lancha'), ('jetski/moto de agua', 'Jetski/Moto de Agua'), ('regata', 'Regata'), ('kayac/canoa', 'Kayac/Canoa'), ('catamaran', 'Catamaran'), ('de pesca', 'De pesca'), ('superyate', 'Superyate'), ('otro', 'Otro')], max_length=60),
        ),
    ]
