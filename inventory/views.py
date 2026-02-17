from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product
from .forms import ProductForm


def product_list(request):
    """List all products."""
    products = Product.objects.select_related("category").all().order_by("name")
    product_data = []
    for p in products:
        product_data.append({"product": p, "stock": p.current_stock()})
    return render(request, "inventory/product_list.html", {"product_data": product_data})


def product_detail(request, pk):
    """View a single product."""
    product = get_object_or_404(Product.objects.select_related("category").prefetch_related("suppliers"), pk=pk)
    stock = product.current_stock()
    return render(request, "inventory/product_detail.html", {"product": product, "stock": stock})


@login_required
def product_create(request):
    """Create a new product."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect("inventory:product_detail", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "inventory/product_form.html", {"form": form, "title": "Add Product"})


@login_required
def product_update(request, pk):
    """Update an existing product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect("inventory:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "inventory/product_form.html", {"form": form, "title": "Edit Product", "product": product})


@login_required
def product_delete(request, pk):
    """Delete a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted successfully.')
        return redirect("inventory:product_list")
    return render(request, "inventory/product_confirm_delete.html", {"product": product})
