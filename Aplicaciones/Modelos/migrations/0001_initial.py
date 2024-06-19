# Generated by Django 5.0.4 on 2024-06-12 00:36

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
                ('precio_estimado', models.DecimalField(decimal_places=1, max_digits=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FotoOferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='archivos-estaticos/fotos_ofertas/')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='Modelos.oferta')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('precio_minimo', models.DecimalField(decimal_places=1, max_digits=10)),
                ('tipo_embarcacion', models.CharField(choices=[('barco', 'Barco'), ('velero', 'Velero'), ('yate', 'Yate'), ('lancha', 'Lancha'), ('jetski/moto de agua', 'Jetski/Moto de Agua'), ('regata', 'Regata'), ('kayac/canoa', 'Kayac/Canoa'), ('catamaran', 'Catamaran'), ('de pesca', 'De pesca'), ('superyate', 'Superyate'), ('otro', 'Otro')], max_length=60)),
                ('anio', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2024)])),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('validada', 'Validada'), ('eliminada', 'Eliminada')], default='pendiente', max_length=10)),
                ('oferta_aceptada', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publicacion_ofertada', to='Modelos.oferta')),
            ],
        ),
        migrations.AddField(
            model_name='oferta',
            name='publicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas_publicacion', to='Modelos.publicacion'),
        ),
        migrations.CreateModel(
            name='Intercambios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], default='aceptado', max_length=10)),
                ('fecha_aceptacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intercambios', to='Modelos.publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='FotoPublicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='archivos-estaticos/fotos_publicaciones/')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='Modelos.publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('dni', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)])),
                ('fecha_nacimiento', models.DateField()),
                ('bloqueado', models.BooleanField(default=False)),
                ('contador_ingresos_fallidos', models.IntegerField(default=0)),
                ('fecha_bloqueo', models.DateTimeField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='Los grupos a los que pertenece el usuario', related_name='mis_usuarios_personalizados', to='auth.group', verbose_name='grupos')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Permisos específicos para este usuario.', related_name='mis_permisos_personalizados', to='auth.permission', verbose_name='permisos de usuario')),
            ],
            options={
                'verbose_name': 'Mi modelo de usuario',
                'verbose_name_plural': 'Mis modelos de usuario',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RoomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unread_messages', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Modelos.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(related_name='roomsUser', through='Modelos.RoomUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publicacion',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='oferta',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas_autor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userN', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-fecha',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('foto', models.ImageField(upload_to='archivos-estaticos/fotos_chats/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='Modelos.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
    ]
