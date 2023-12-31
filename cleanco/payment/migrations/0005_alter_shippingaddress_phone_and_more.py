# Generated by Django 4.2.4 on 2023-10-04 17:07

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0004_shippingaddress_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shippingaddress",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="state",
            field=models.CharField(default="", max_length=255),
        ),
    ]
