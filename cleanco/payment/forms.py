from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress

        fields = ["full_name", "email", "phone", "state", "city", "warehouse_number"]

        exclude = [
            "user",
        ]
