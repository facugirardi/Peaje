# Generated by Django 4.2.4 on 2023-11-03 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('direccion', models.CharField(max_length=50, verbose_name='Direccion')),
                ('tipo_documento', models.CharField(max_length=50, verbose_name='Tipo Documento')),
                ('numero_documento', models.CharField(max_length=50, verbose_name='Numero Documento')),
                ('permisos', models.BooleanField(default=False, verbose_name='Admin')),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponible')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Casilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_casilla', models.IntegerField(verbose_name='Numero Casilla:')),
                ('estado', models.BooleanField(default=True, verbose_name='Abierto:')),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Ruta:')),
                ('tipo', models.CharField(choices=[('Nacional', 'Nacional'), ('Provincial', 'Provincial')], max_length=50, verbose_name='Tipo Ruta:')),
                ('coordenadas', models.CharField(max_length=50, verbose_name='Coordenada Ruta:')),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(choices=[('motocicleta', 'Motocicleta'), ('automoviles', 'Automóviles'), ('2_ejes_duales', '2 Ejes con Ruedas Duales o Altura Mayor a 2.10m'), ('3_4_ejes', '3 o 4 Ejes, Sin Ruedas Duales y Altura Menor a 2.10m'), ('3_4_ejes2', '3 o 4 Ejes, Con Ruedas Duales o Altura Mayor a 2,10m'), ('5_6_ejes', '5 o 6 Ejes'), ('mas_de_6_ejes', 'Más de 6 Ejes')], max_length=50, verbose_name='Categoria Vehiculo')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Monto:')),
                ('fecha_modificacion', models.DateField(verbose_name='Fecha Modificacion:')),
            ],
        ),
        migrations.CreateModel(
            name='TurnoTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fh_inicio', models.DateTimeField(verbose_name='Fecha y Hora Incio:')),
                ('fh_fin', models.DateTimeField(verbose_name='Fecha y Hora Final:')),
                ('sentido_cobro', models.CharField(max_length=100, verbose_name='Sentido de Cobro:')),
                ('monto_inicial', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Monto Inicial:')),
                ('enlace_reporte', models.CharField(default='NULL', max_length=50, verbose_name='Enlace Reporte:')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado:')),
                ('casilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peajeApp.casilla')),
                ('usuario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroCobro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fh_emision', models.DateTimeField(verbose_name='Fecha y Hora Emision:')),
                ('patente', models.CharField(default='NULL', max_length=24, verbose_name='Patente:')),
                ('tarifa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peajeApp.tarifa')),
                ('turno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peajeApp.turnotrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='Estacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_estacion', models.IntegerField(verbose_name='Numero Estacion:')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Estacion:')),
                ('km_ruta', models.IntegerField(verbose_name='KM Ruta:')),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peajeApp.ruta')),
            ],
        ),
        migrations.AddField(
            model_name='casilla',
            name='estacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peajeApp.estacion'),
        ),
    ]
