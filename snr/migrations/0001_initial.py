# Generated by Django 4.0 on 2023-02-25 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_category_product'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderd_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('order_id', models.CharField(blank=True, default=None, max_length=130, null=True, unique=True)),
                ('date_timeofpayment', models.DateTimeField(auto_now_add=True)),
                ('order_deliverd', models.BooleanField(default=False)),
                ('order_reciverd', models.BooleanField(default=False)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=200, null=True)),
                ('items', models.ManyToManyField(to='snr.orderd_item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name': 'orderItm',
                'verbose_name_plural': 'orderditm',
            },
        ),
    ]
