# Generated by Django 4.1.1 on 2022-09-15 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_adminuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminuser',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
