# Generated by Django 5.0 on 2023-12-16 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
