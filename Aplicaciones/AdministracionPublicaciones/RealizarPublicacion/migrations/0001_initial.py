# Generated by Django 5.0.6 on 2024-05-17 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('precio_minimo', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tipo_embarcacion', models.CharField(max_length=50)),
                ('anio', models.IntegerField()),
                ('foto', models.ImageField(default='static/images/default.png', upload_to='publicaciones_fotos/')),
            ],
        ),
    ]
