# Generated by Django 4.2.4 on 2023-10-04 16:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0002_order_orderitem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="address1",
            new_name="address",
        ),
        migrations.RemoveField(
            model_name="shippingaddress",
            name="address2",
        ),
    ]
