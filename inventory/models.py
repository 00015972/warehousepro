from django.db import models
from django.db.models import Sum, Q

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Customer(TimeStampedModel):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=60, unique=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    # many-to-one
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")

    # many-to-many
    suppliers = models.ManyToManyField(Supplier, related_name="products", blank=True)

    # optional media
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

    def current_stock(self) -> int:
        agg = self.movements.aggregate(
            total_in=Sum("quantity", filter=Q(movement_type="IN")),
            total_out=Sum("quantity", filter=Q(movement_type="OUT")),
        )
        total_in = agg.get("total_in") or 0
        total_out = agg.get("total_out") or 0
        return total_in - total_out
