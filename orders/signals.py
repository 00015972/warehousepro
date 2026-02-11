from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from stock.models import StockMovement
from .models import PurchaseOrder, SalesOrder


@receiver(pre_save, sender=PurchaseOrder)
def po_store_previous_status(sender, instance: PurchaseOrder, **kwargs):
    if instance.pk:
        instance._prev_status = PurchaseOrder.objects.get(pk=instance.pk).status
    else:
        instance._prev_status = None


@receiver(post_save, sender=PurchaseOrder)
def po_create_stock_on_received(sender, instance: PurchaseOrder, created: bool, **kwargs):
    prev = getattr(instance, "_prev_status", None)
    if prev != PurchaseOrder.Status.RECEIVED and instance.status == PurchaseOrder.Status.RECEIVED:
        with transaction.atomic():
            for item in instance.items.select_related("product").all():
                StockMovement.objects.create(
                    product=item.product,
                    movement_type=StockMovement.MovementType.IN,
                    reference_type=StockMovement.ReferenceType.PO,
                    reference_id=str(instance.id),
                    quantity=item.quantity,
                    note="Auto IN from Purchase Order received",
                    created_by=instance.created_by,
                )


@receiver(pre_save, sender=SalesOrder)
def so_store_previous_status(sender, instance: SalesOrder, **kwargs):
    if instance.pk:
        instance._prev_status = SalesOrder.objects.get(pk=instance.pk).status
    else:
        instance._prev_status = None


@receiver(post_save, sender=SalesOrder)
def so_create_stock_on_shipped(sender, instance: SalesOrder, created: bool, **kwargs):
    prev = getattr(instance, "_prev_status", None)
    if prev != SalesOrder.Status.SHIPPED and instance.status == SalesOrder.Status.SHIPPED:
        with transaction.atomic():
            for item in instance.items.select_related("product").all():
                StockMovement.objects.create(
                    product=item.product,
                    movement_type=StockMovement.MovementType.OUT,
                    reference_type=StockMovement.ReferenceType.SO,
                    reference_id=str(instance.id),
                    quantity=item.quantity,
                    note="Auto OUT from Sales Order shipped",
                    created_by=instance.created_by,
                )
