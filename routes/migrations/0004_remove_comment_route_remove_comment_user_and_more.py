# Generated by Django 5.1.7 on 2025-03-22 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_alter_routelocation_options_remove_route_locations_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='route',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='like',
            name='route',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.RemoveField(
            model_name='routeimage',
            name='route',
        ),
        migrations.RemoveField(
            model_name='routelocation',
            name='route',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='RouteImage',
        ),
        migrations.DeleteModel(
            name='RouteLocation',
        ),
    ]
