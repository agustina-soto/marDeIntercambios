# Generated by Django 5.0.4 on 2024-06-30 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0022_alter_fotopublicidad_foto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotopublicidad',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='archivos-estaticos/publicidades/'),
        ),
    ]