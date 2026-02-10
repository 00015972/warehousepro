from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "product", "movement_type", "quantity", "reference_type", "reference_id", "created_by")
    list_filter = ("movement_type", "reference_type")
    search_fields = ("product__name", "product__sku", "reference_id")

