# Generated by Django 5.0.4 on 2024-07-01 19:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0018_alter_publicacion_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambios',
            name='calificacion_autor',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AddField(
            model_name='intercambios',
            name='calificacion_comprador',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AddField(
            model_name='intercambios',
            name='descripcion_autor',
            field=models.TextField(blank=True),
        ),
    ]