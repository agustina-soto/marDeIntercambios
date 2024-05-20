# Generated by Django 5.0.6 on 2024-05-19 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RealizarPublicacion', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='foto',
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='tipo_embarcacion',
            field=models.CharField(choices=[('Yate', 'Yate'), ('Lancha', 'Lancha'), ('Jetski/Moto de Agua', 'Jetski/Moto de Agua'), ('Velero', 'Velero'), ('Regata', 'Regata'), ('Kayac/Canoa', 'Kayac/Canoa'), ('Catamaran', 'Catamaran'), ('De pesca', 'De pesca'), ('Superyate', 'Superyate'), ('Otro', 'Otro')], max_length=60),
        ),
        migrations.CreateModel(
            name='FotoPublicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='publicaciones_fotos/')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='RealizarPublicacion.publicacion')),
            ],
        ),
    ]
