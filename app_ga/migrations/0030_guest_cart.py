# Generated by Django 4.0.6 on 2022-10-01 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0029_products_dis_perc'),
    ]

    operations = [
        migrations.CreateModel(
            name='guest_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=100)),
                ('total_price', models.CharField(max_length=100)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.products')),
            ],
        ),
    ]
