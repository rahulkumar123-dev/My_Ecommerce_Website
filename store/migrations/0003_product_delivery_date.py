# Generated by Django 5.2.4 on 2025-07-17 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_delivery_estimate_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delivery_date',
            field=models.DateField(blank=True, help_text='Override delivery date', null=True),
        ),
    ]
