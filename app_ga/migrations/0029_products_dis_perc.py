# Generated by Django 4.0.6 on 2022-10-01 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0028_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='dis_perc',
            field=models.BigIntegerField(null=True),
        ),
    ]
