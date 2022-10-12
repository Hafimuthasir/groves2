# Generated by Django 4.0.6 on 2022-10-12 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.CreateModel(
            name='admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=True, upload_to='static/uploadedproducts')),
                ('image2', models.ImageField(default=True, upload_to='static/uploadedproducts')),
                ('image3', models.ImageField(default=True, upload_to='static/uploadedproducts')),
            ],
        ),
        migrations.CreateModel(
            name='carbrands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carbrand', models.CharField(default=True, max_length=100)),
                ('carlogo', models.ImageField(default=True, upload_to='static/uploadedproducts')),
            ],
        ),
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to='static/catgoryicons')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_number', models.CharField(max_length=16)),
                ('start_date', models.DateTimeField(auto_now=True)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(null=True)),
                ('discount_percentage', models.IntegerField(null=True)),
                ('expiry_date', models.DateTimeField()),
                ('minimum_amount', models.IntegerField(default=500)),
            ],
        ),
        migrations.CreateModel(
            name='monthly_sales_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='myusers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phonenumber', models.BigIntegerField()),
                ('status', models.BooleanField(max_length=20, null=True)),
                ('refferal_code', models.CharField(max_length=50)),
                ('applied_coupons', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='prodbrands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productbrand', models.CharField(default=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('productname', models.CharField(max_length=100)),
                ('price', models.BigIntegerField()),
                ('dis_price', models.BigIntegerField(null=True)),
                ('dis_price_type', models.CharField(max_length=100, null=True)),
                ('dis_proprice', models.BigIntegerField(null=True)),
                ('total_disprice', models.BigIntegerField(null=True)),
                ('dis_perc', models.BigIntegerField(null=True)),
                ('dis_applied', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=100)),
                ('stocks', models.CharField(default='1', max_length=100)),
                ('stock_status', models.BooleanField(default=True)),
                ('category', models.CharField(max_length=100)),
                ('retrn', models.BooleanField(default=True)),
                ('retrn_policy', models.CharField(max_length=10, null=True)),
                ('carbrand', models.CharField(max_length=100)),
                ('prodbrand', models.CharField(max_length=100)),
                ('image', models.ImageField(default=True, upload_to='static/uploadedproducts')),
                ('image2', models.ImageField(upload_to='static/uploadedproducts')),
                ('image3', models.ImageField(upload_to='static/uploadedproducts')),
                ('image4', models.ImageField(upload_to='static/uploadedproducts')),
                ('carbrid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.carbrands')),
                ('catid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_ga.categories')),
                ('prodid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_ga.prodbrands')),
            ],
        ),
        migrations.CreateModel(
            name='sales_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
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
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=100)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.products')),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.myusers')),
            ],
        ),
        migrations.CreateModel(
            name='recent_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.products')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.myusers')),
            ],
        ),
        migrations.CreateModel(
            name='guest_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_session', models.CharField(max_length=20)),
                ('quantity', models.CharField(max_length=100)),
                ('total_price', models.CharField(max_length=100, null=True)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.products')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=100)),
                ('total_price', models.CharField(max_length=100)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.products')),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_ga.myusers')),
            ],
        ),
    ]
