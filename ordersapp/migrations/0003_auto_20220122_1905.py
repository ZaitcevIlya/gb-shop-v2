# Generated by Django 3.2.8 on 2022-01-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0002_auto_20220122_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='update',
        ),
        migrations.AddField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
