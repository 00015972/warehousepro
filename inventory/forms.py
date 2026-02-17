from django import forms
from .models import Product, Category, Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "unit_price", "reorder_level", "category", "suppliers", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "sku": forms.TextInput(attrs={"class": "form-input"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-input"}),
            "category": forms.Select(attrs={"class": "form-input"}),
            "suppliers": forms.SelectMultiple(attrs={"class": "form-input"}),
        }
