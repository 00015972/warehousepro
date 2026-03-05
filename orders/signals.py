from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import PurchaseOrder, SalesOrder


@receiver(pre_save, sender=PurchaseOrder)
def po_store_previous_status(sender, instance: PurchaseOrder, **kwargs):
    """Store the previous status before saving."""
    if instance.pk:
        try:
            instance._prev_status = PurchaseOrder.objects.get(pk=instance.pk).status
        except PurchaseOrder.DoesNotExist:
            instance._prev_status = None
    else:
        instance._prev_status = None


@receiver(pre_save, sender=SalesOrder)
def so_store_previous_status(sender, instance: SalesOrder, **kwargs):
    """Store the previous status before saving."""
    if instance.pk:
        try:
            instance._prev_status = SalesOrder.objects.get(pk=instance.pk).status
        except SalesOrder.DoesNotExist:
            instance._prev_status = None
    else:
        instance._prev_status = None


def create_po_stock_movements(order: PurchaseOrder):
    """Create IN stock movements when PO status changes to RECEIVED."""
    from stock.models import StockMovement

    # Check if we already created movements for this order
    existing = StockMovement.objects.filter(
        reference_type=StockMovement.ReferenceType.PO,
        reference_id=str(order.id)
    ).exists()

    if existing:
        return  # Already processed

    with transaction.atomic():
        for item in order.items.select_related("product").all():
            StockMovement.objects.create(
                product=item.product,
                movement_type=StockMovement.MovementType.IN,
                reference_type=StockMovement.ReferenceType.PO,
                reference_id=str(order.id),
                quantity=item.quantity,
                note=f"Auto IN from Purchase Order #{order.id}",
                created_by=order.created_by,
            )


def create_so_stock_movements(order: SalesOrder):
    """Create OUT stock movements when SO status changes to SHIPPED."""
    from stock.models import StockMovement

    # Check if we already created movements for this order
    existing = StockMovement.objects.filter(
        reference_type=StockMovement.ReferenceType.SO,
        reference_id=str(order.id)
    ).exists()

    if existing:
        return  # Already processed

    with transaction.atomic():
        for item in order.items.select_related("product").all():
            StockMovement.objects.create(
                product=item.product,
                movement_type=StockMovement.MovementType.OUT,
                reference_type=StockMovement.ReferenceType.SO,
                reference_id=str(order.id),
                quantity=item.quantity,
                note=f"Auto OUT from Sales Order #{order.id}",
                created_by=order.created_by,
            )
