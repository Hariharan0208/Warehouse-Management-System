# Generated by Django 5.1.2 on 2024-12-11 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_producttable_specifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='Specifications',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
