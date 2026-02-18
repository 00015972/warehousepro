from django.shortcuts import render

from inventory.models import Product
from .models import StockMovement
# Create your views here.


def dashboard(request):
    products = Product.objects.all()

    low_stock_products = []
    for p in products:
        stock = p.current_stock()
        if stock <= p.reorder_level:
            low_stock_products.append((p, stock))

    recent_movements = StockMovement.objects.select_related("product").order_by("-created_at")[:10]

    context = {
        "low_stock_products": low_stock_products,
        "recent_movements": recent_movements,
    }
    return render(request, "stock/dashboard.html", context)
