# Generated by Django 5.0.6 on 2024-06-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0005_publicacion_estado_alter_oferta_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=10),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='precio_estimado',
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('validada', 'Validada'), ('eliminada', 'Eliminada')], default='pendiente', max_length=10),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='precio_minimo',
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
    ]