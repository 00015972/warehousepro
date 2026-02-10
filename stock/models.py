from django.conf import settings
from django.db import models

from inventory.models import Product


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "IN", "IN"
        OUT = "OUT", "OUT"
        ADJUSTMENT = "ADJ", "ADJUSTMENT"

    class ReferenceType(models.TextChoices):
        PO = "PO", "Purchase Order"
        SO = "SO", "Sales Order"
        MANUAL = "MANUAL", "Manual"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="movements")
    movement_type = models.CharField(max_length=3, choices=MovementType.choices)
    reference_type = models.CharField(max_length=10, choices=ReferenceType.choices, default=ReferenceType.MANUAL)
    reference_id = models.CharField(max_length=64, blank=True)  # store order id as string for simplicity
    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="stock_movements")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.movement_type} {self.quantity} x {self.product.sku}"

