# Generated by Django 5.0.4 on 2024-06-09 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0008_room_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='archivos-estaticos/fotos_ofertas/'),
        ),
    ]