# Generated by Django 4.0 on 2023-03-01 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snr', '0004_rename_countries_checkout_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkout',
            options={'verbose_name': 'Checkoutlist', 'verbose_name_plural': 'checkoutlist'},
        ),
    ]
