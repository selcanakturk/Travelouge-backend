# Generated by Django 5.1.7 on 2025-03-19 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),
    ]
