# Generated by Django 4.0.6 on 2022-09-02 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_ga', '0005_alter_products_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='carbrands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carbrand', models.CharField(default=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='carbrid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.carbrands'),
        ),
    ]