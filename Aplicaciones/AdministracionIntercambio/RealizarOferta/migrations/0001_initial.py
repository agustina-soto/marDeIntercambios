# Generated by Django 5.0.4 on 2024-06-04 09:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('RealizarPublicacion', '0003_publicacion_estado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_estimado', models.DecimalField(decimal_places=2, max_digits=7)),
                ('descripcion', models.TextField(max_length=260)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to=settings.AUTH_USER_MODEL)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oferta', to='RealizarPublicacion.publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='FotoOferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='archivos-estaticos/fotos_ofertas/')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='RealizarOferta.oferta')),
            ],
        ),
    ]
