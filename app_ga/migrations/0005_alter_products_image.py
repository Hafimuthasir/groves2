# Generated by Django 4.0.6 on 2022-09-02 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0004_prodbrands_products_prodbrand_products_prodid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default=True, upload_to='static/uploadedproducts'),
        ),
    ]
