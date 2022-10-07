# Generated by Django 4.0.6 on 2022-10-07 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0031_recent_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('categoryName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('productPrice', models.FloatField()),
            ],
        ),
    ]