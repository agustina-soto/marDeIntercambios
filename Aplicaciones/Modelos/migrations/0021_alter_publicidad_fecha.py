# Generated by Django 5.0.4 on 2024-06-30 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0020_alter_publicidad_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicidad',
            name='fecha',
            field=models.DateField(),
        ),
    ]
