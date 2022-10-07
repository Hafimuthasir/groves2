# Generated by Django 4.0.6 on 2022-09-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('buyer_name', models.CharField(max_length=50)),
                ('buyer_phone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=7)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
    ]
