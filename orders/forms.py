from django import forms
from .models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ["supplier", "status", "notes"]
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
        }


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ["product", "quantity", "unit_cost"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-input"}),
            "quantity": forms.NumberInput(attrs={"class": "form-input"}),
            "unit_cost": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
        }


PurchaseOrderItemFormSet = forms.inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=1,
    can_delete=True,
)


class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ["customer", "status", "notes"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
        }


class SalesOrderItemForm(forms.ModelForm):
    class Meta:
        model = SalesOrderItem
        fields = ["product", "quantity", "unit_price"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-input"}),
            "quantity": forms.NumberInput(attrs={"class": "form-input"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
        }


SalesOrderItemFormSet = forms.inlineformset_factory(
    SalesOrder,
    SalesOrderItem,
    form=SalesOrderItemForm,
    extra=1,
    can_delete=True,
)
