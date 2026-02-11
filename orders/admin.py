from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier", "status", "created_by", "created_at")
    list_filter = ("status",)
    inlines = [PurchaseOrderItemInline]


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_by", "created_at")
    list_filter = ("status",)
    inlines = [SalesOrderItemInline]

