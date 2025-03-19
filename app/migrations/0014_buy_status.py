# Generated by Django 5.1.2 on 2024-12-10 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_buy_loaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='status',
            field=models.CharField(choices=[('dispatched', 'Dispatched'), ('in_transit', 'In Transit'), ('delivered', 'Delivered')], max_length=50, null=True),
        ),
    ]
