# Generated by Django 5.1.2 on 2024-11-30 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='Agent',
            field=models.CharField(default='No', max_length=30, null=True),
        ),
    ]
