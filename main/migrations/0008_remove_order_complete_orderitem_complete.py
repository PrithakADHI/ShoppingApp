# Generated by Django 4.2.7 on 2023-11-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_order_orderitem_order_products_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complete',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
