from django.contrib import admin
from .models import Category, Supplier, Customer, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ("name", "email")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "unit_price", "reorder_level")
    list_filter = ("category",)
    search_fields = ("name", "sku")
