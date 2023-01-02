# Generated by Django 4.1.4 on 2023-01-02 04:23

import accounts.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(8, message='8자 이상 입력해주세요..!')], verbose_name='password')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'normal_user',
                'verbose_name_plural': 'normal_users',
                'db_table': 'normal_user',
            },
        ),
        migrations.CreateModel(
            name='LoginRecodeData',
            fields=[
                ('normal_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.normaluser')),
                ('ip', models.CharField(max_length=15)),
                ('country_code', models.CharField(default='XX', max_length=2)),
                ('country_name', models.CharField(default='UNKNOWN', max_length=100)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NormalUserPermission',
            fields=[
                ('normal_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.normaluser')),
                ('adv', models.BooleanField(verbose_name='adv_accept')),
                ('permission', models.BooleanField(verbose_name='permission_accept')),
                ('check_email', models.BooleanField(verbose_name='cheking_email')),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=6, verbose_name='name')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'admin_user',
                'verbose_name_plural': 'admin_users',
                'db_table': 'admin_user',
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]
