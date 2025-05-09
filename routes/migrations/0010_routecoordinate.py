# Generated by Django 5.1.7 on 2025-04-15 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0009_route_coordinates'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteCoordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_coordinates', to='routes.route')),
            ],
        ),
    ]
