# Generated by Django 4.0.6 on 2022-09-23 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0016_carbrands_carlogo'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusers',
            name='refferal_code',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
