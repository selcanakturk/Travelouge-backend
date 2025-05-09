# Generated by Django 5.1.7 on 2025-03-22 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_route_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='image',
        ),
        migrations.CreateModel(
            name='RouteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='routes/images/')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='routes.route')),
            ],
        ),
    ]
