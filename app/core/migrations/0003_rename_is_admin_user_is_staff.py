# Generated by Django 4.0.2 on 2022-02-25 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_is_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='is_staff',
        ),
    ]
